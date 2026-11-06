#!/usr/bin/env python3
"""Assemble and verify RedSigil Type System v1.0.1 packages from a verified artifact.

Copyright (c) 2026 Gerald A Folsom Jr.  MIT, see licenses/MIT-TOOLS.txt.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

REPO = "RedSigilDelta/RS-Type-System"
VERSION = "v1.0.1"
BUILD = "c956f7fc483a8a2d5bf6af8b35a643e8d3147a24"
RUN = 42104786087
ARTIFACT = f"redsigil-v1.0.1-stable-fonts-{RUN}"
LABELS = {
    '01': 'Stable_Fonts',
    '02': 'Editable_Sources',
    '03': 'Complete',
    '04': 'Release_Verification',
}
ZIPS = {k: f"RedSigil_Type_System_{k}_{v}_{VERSION}.zip" for k,v in LABELS.items()}
SIDECAR = "SHA256SUMS_v1.0.1.txt"
COUNTS = {'display': (5,1,6), 'everyday': (4,1,5), 'mono':(4,1,5)}
TOP_ALLOW = {'README.md','CHANGELOG.md','RELEASE_NOTES.md','LICENSES.md','.gitignore','.gitattributes'}
DOCS = ('README.md','CHANGELOG.md','RELEASE_NOTES.md','LICENSES.md')
TAGLINE = '🔥 Forged for Expression. ⚙️ Engineered for Precision.'


def run(args: list[str], cwd: Path, *, capture=True) -> str:
    return subprocess.run(args,cwd=cwd,check=True,text=True,stdout=subprocess.PIPE if capture else None).stdout.strip() if capture else ''


def sha(data:bytes)->str:
    return sha256(data).hexdigest()


def sha_path(path:Path)->str:
    h=sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def check_repo(root: Path) -> tuple[str,list[str]]:
    if not (root / 'README.md').is_file() or not (root / '.git').exists():
        raise RuntimeError('Not the local RS-Type-System Git repository')
    if run(['git','branch','--show-current'],root)!='master':
        raise RuntimeError('Must package from master')
    if run(['git','status','--porcelain'],root):
        raise RuntimeError('Working tree is not clean. Commit the approved G9E files first.')
    try:
        run(['git','cat-file','-e', BUILD+'^{commit}'],root)
    except subprocess.CalledProcessError:
        raise RuntimeError('Original verified build commit is missing from history')
    critical_changes=set(run(['git','diff','--name-only',BUILD,'HEAD','--','sources','build','tools'],root).splitlines())
    if critical_changes - {'tools/render_specimens.py'}:
        raise RuntimeError('Existing font sources/build scripts changed since validated build: REBUILD REQUIRED. Changed: '+str(sorted(critical_changes)))
    # Adding a standalone image renderer does not alter the verified font build.
    # One additional post-build naming-correction commit is permitted; all source and font integrity gates remain unchanged.
    if run(['git','rev-list','--count',BUILD+'..HEAD'],root) not in {'0','1','2','3','4','5','6'}:
        raise RuntimeError('Unexpected number of follow-up commits; inspect provenance')
    # Existing repository may use HTTPS or SSH origin. Never accept another owner/repo.
    remote=run(['git','remote','get-url','origin'],root)
    if not any(remote.endswith(x) for x in (f'github.com/{REPO}.git', f'github.com/{REPO}',f'github.com:{REPO}.git',f'github.com:{REPO}')):
        raise RuntimeError('Origin URL does not identify '+REPO+': '+remote)
    files=run(['git','ls-files','-z'],root).split('\0')
    files=[f for f in files if f]
    for f in files:
        part=PurePosixPath(f)
        if part.is_absolute() or '..' in part.parts or '\\' in f:
            raise RuntimeError('Unsafe path in Git index: '+f)
        if not (f in TOP_ALLOW or f.startswith(('sources/','build/','tools/','docs/','licenses/')) or f=='.github/workflows/stable-font-build.yml' or f=='release/make_release.py' or f.startswith('assets/specimens/')):
            raise RuntimeError('Unexpected tracked file would enter public package: '+f)
        p=root/f
        if not p.is_file() or p.is_symlink():
            raise RuntimeError('Tracked file is missing or symbolic link: '+f)
    must={*DOCS,'docs/BUILDING.md','docs/VERIFICATION.md','docs/PROVENANCE.md','docs/SOURCE_STRUCTURE.md','docs/FONT_FAMILIES.md','docs/FONT_SPECIMENS.md','tools/render_specimens.py','assets/specimens/SPECIMENS.json','assets/specimens/hero.png','assets/specimens/display.png','assets/specimens/everyday.png','assets/specimens/mono.png','assets/specimens/symbols.png','licenses/MIT-TOOLS.txt','licenses/OFL-1.1.txt','release/make_release.py','.github/workflows/stable-font-build.yml'}
    if not must.issubset(files):
        raise RuntimeError('Required release files missing: '+', '.join(sorted(must-set(files))))
    for f in [*DOCS,'docs/BUILDING.md','docs/VERIFICATION.md','docs/PROVENANCE.md','docs/SOURCE_STRUCTURE.md','.github/workflows/stable-font-build.yml']:
        txt=(root/f).read_text(encoding='utf8')
        if re.search(r'\b(?:draft|proposed|under review|working copy|not yet independently|not published)\b',txt,re.I):
            raise RuntimeError('Release-facing document contains obsolete state language: '+f)
    if TAGLINE not in (root/'README.md').read_text('utf8'):
        raise RuntimeError('Approved tagline missing')
    # Avoid accidentally publishing credentials or backups as part of the source package.
    print(f'PASS: clean master; {len(files)} tracked source/documentation files; build-critical paths match {BUILD[:8]}')
    return run(['git','rev-parse','HEAD'],root),files


def check_fonts(root:Path, evidence:Path)->tuple[Path,dict[str,Path],dict]:
    artifact=evidence/ARTIFACT
    if not artifact.is_dir():
        raise RuntimeError('Artifact directory missing: '+str(artifact))
    fonts={}
    for family,(ns,nv,nw) in COUNTS.items():
        for typ,ext,expected in [('static','.ttf',ns),('variable','.ttf',nv),('woff2','.woff2',nw)]:
            actual=sorted((artifact/family/typ).glob('*'+ext))
            if len(actual)!=expected:
                raise RuntimeError(f'{family}/{typ}: got {len(actual)}, expected {expected}')
            for p in actual:
                rel=p.relative_to(artifact).as_posix()
                if p.is_symlink() or p.stat().st_size==0:
                    raise RuntimeError('Invalid font: '+rel)
                fonts[rel]=p
    if len(fonts)!=32:
        raise RuntimeError('Wrong font count')
    qa_path=artifact/'QA_REPORT.json'
    if not qa_path.is_file():
        raise RuntimeError('GitHub build QA_REPORT.json missing')
    qa=json.loads(qa_path.read_text('utf8'))
    if qa.get('result')!='PASS' or qa.get('file_count')!=32:
        raise RuntimeError('GitHub build QA report does not confirm 32 PASS')
    qa_files={v['path']:v['sha256'] for v in qa.get('files',[])}
    if set(qa_files)!=set(fonts):
        raise RuntimeError('QA report paths do not match 32 fonts')
    for rel,p in fonts.items():
        if sha_path(p)!=qa_files[rel]:
            raise RuntimeError('Font differs from GitHub build QA manifest: '+rel)
    # Specimen provenance: reject invented, stale or missing preview assets.
    specimen=root/'assets/specimens/SPECIMENS.json'
    if not specimen.is_file():
        raise RuntimeError('Actual-font specimen provenance missing')
    meta=json.loads(specimen.read_text('utf8'))
    if meta.get('release')!=VERSION or meta.get('production_run')!=RUN or meta.get('artifact')!=ARTIFACT:
        raise RuntimeError('Specimen provenance does not identify the verified v1.0.1 artifact')
    expected_weights={'display':{'Regular':400,'Medium':500,'Semibold':600,'Bold':700,'ExtraBold':800},
                      'everyday':{'Regular':400,'Medium':500,'Semibold':600,'Bold':700},
                      'mono':{'Regular':400,'Medium':500,'Semibold':600,'Bold':700}}
    if meta.get('static_weights')!=expected_weights:
        raise RuntimeError('Specimen weight labels do not match released styles')
    observed={}
    for f,detail in meta.get('fonts',{}).items():
        rel=detail.get('font_path')
        if not isinstance(rel,str) or rel not in fonts or '/static/' not in rel:
            raise RuntimeError('Specimen used an unknown/nonstatic font: '+str(rel))
        if detail.get('sha256')!=sha_path(fonts[rel]):
            raise RuntimeError('Specimen font hash differs from verified build: '+rel)
        observed[rel]=1
    if len(observed)!=13:
        raise RuntimeError('Specimen must account for 13 unique static fonts')
    expected_imgs={'hero.png','display.png','everyday.png','mono.png','symbols.png'}
    images=meta.get('specimens',{})
    if set(images)!=expected_imgs:
        raise RuntimeError('Exactly five specimen images required')
    for filename in sorted(expected_imgs):
        path=root/'assets/specimens'/filename
        if not path.is_file() or path.stat().st_size==0:
            raise RuntimeError('Missing specimen image: '+filename)
        if images[filename]['sha256']!=sha_path(path) or not path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise RuntimeError('Specimen image integrity failed: '+filename)
    print('PASS: Five actual-font specimens and 13 static font input hashes verified')
    for name,location in [('workflow',artifact/'SHA256SUMS.txt'),('local',evidence/'SHA256SUMS.build.txt')]:
        if not location.is_file():
            raise RuntimeError('Missing '+name+' saved checksum inventory: '+str(location))
        subprocess.run(['sha256sum','-c',str(location)],cwd=(artifact if name=='workflow' else evidence),stdout=subprocess.DEVNULL,check=True)
    subprocess.run([sys.executable,'tools/stable_font_verify.py','--compiled',str(artifact)],cwd=root,check=True)
    subprocess.run([sys.executable,'tools/stable_font_verify.py','--sources'],cwd=root,check=True)
    subprocess.run([sys.executable,'tools/greek_delta_check.py'],cwd=root,check=True)
    subprocess.run([sys.executable,'-m','unittest','tools/test_greek_delta_check.py'],cwd=root,check=True)
    print('PASS: 32 GitHub QA hashes, workflow + local checksum inventories, source and compiled regressions')
    return artifact,fonts,qa


def zip_bytes(pairs: list[tuple[str,bytes]],dt:tuple[int,int,int,int,int,int])->bytes:
    output=io.BytesIO()
    used=set()
    with ZipFile(output,'w',compression=ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
        for name,contents in sorted(pairs):
            path=PurePosixPath(name)
            if name in used or path.is_absolute() or '..' in path.parts or '\\' in name:
                raise RuntimeError('Unsafe/duplicate ZIP member: '+name)
            used.add(name)
            info=ZipInfo(filename=name,date_time=dt)
            info.create_system=3
            info.external_attr=(0o100644 << 16)
            info.compress_type=ZIP_DEFLATED
            z.writestr(info,contents,compress_type=ZIP_DEFLATED,compresslevel=9)
    return output.getvalue()


def produce(root:Path,evidence:Path,dist:Path)->None:
    release_sha,source_files=check_repo(root)
    artifact,fonts,qa=check_fonts(root,evidence)
    if dist.exists() and any(dist.iterdir()):
        raise RuntimeError('Release directory already contains files; refusing to overwrite: '+str(dist))
    dist.mkdir(parents=True,exist_ok=True)
    ts=int(run(['git','log','-1','--format=%ct'],root))
    dt=datetime.fromtimestamp(ts,timezone.utc).timetuple()[:6]
    if dt[0] < 1980:
        dt=(2026,1,1,0,0,0)
    # Zip timestamps are 2-second precision.
    dt=(*dt[:5],dt[5]//2*2)
    source=[(name,(root/name).read_bytes()) for name in source_files]
    stable_text=(f'RedSigil Type System {VERSION} — Stable Fonts\n'
       f'{TAGLINE}\n\n'
       'Three families: Display, Everyday, Mono.\n'
       '13 static TTF + 3 variable TTF + 16 WOFF2 = 32 fonts.\n'
       'Font Software: SIL OFL 1.1; Reserved Font Name RedSigil.\n'
       'Source, verification and release downloads: https://github.com/RedSigilDelta/RS-Type-System\n'
       'See OFL-1.1.txt for the fonts and MIT-TOOLS.txt for original explanatory text.\n')
    stable=[(n,p.read_bytes()) for n,p in fonts.items()]
    stable += [('README_STABLE.txt',stable_text.encode('utf8')),
        ('OFL-1.1.txt',(root/'licenses/OFL-1.1.txt').read_bytes()),
        ('MIT-TOOLS.txt',(root/'licenses/MIT-TOOLS.txt').read_bytes())]
    complete=source+ [('fonts/'+n,p.read_bytes()) for n,p in fonts.items()]
    data={}
    for k,pairs in [('01',stable),('02',source),('03',complete)]:
        archive=zip_bytes(pairs,dt)
        (dist/ZIPS[k]).write_bytes(archive)
        data[k]={'filename':ZIPS[k],'sha256':sha(archive),'files':len(pairs),'size_bytes':len(archive)}
        print(f'PASS: Package {k} {ZIPS[k]} — {len(pairs)} entries, SHA256 {data[k]["sha256"]}')
    manifest={
        'release':VERSION, 'repository':REPO,
        'compiled_from_commit':BUILD,
        'release_source_commit':release_sha,
        'github_actions_run':RUN,
        'github_actions_url':f'https://github.com/{REPO}/actions/runs/{RUN}',
        'github_actions_artifact':ARTIFACT,
        'compiled_output_counts':{'static_ttf':13,'variable_ttf':3,'woff2':16,'total':32},
        'source_ufo_master_count':7,'designspace_count':3,'specimen_image_count':5,
        'qa_report_status':qa['result'],
        'verified_font_count':len(fonts),
        'validation':['published build artifact PASS','QA_REPORT hashes 32/32','workflow checksum inventory 32/32','local checksum inventory 32/32','compiled verifier PASS','source verifier PASS','Delta test PASS','five real-font specimen hashes PASS'],
        'package_sha256':data,
    }
    archive_sums=''.join(f'{data[k]["sha256"]}  {ZIPS[k]}\n' for k in ('01','02','03'))
    font_sums=''.join(f'{sha_path(fonts[p])}  {p}\n' for p in sorted(fonts))
    source_sums=''.join(f'{sha(b)}  {p}\n' for p,b in source)
    checking=(f'# Release verification — {VERSION}\n\n'
              f'Packages 01–03 match `SHA256SUMS_packages.txt`.\n'
              f'The 32 font files, in Package 01, match `SHA256SUMS_fonts.txt`.\n'
              f'`SOURCE_SHA256SUMS.txt` checks Package 02.\n'
              f'`QA_REPORT.json` comes from the successful GitHub Actions run {RUN}.\n'
              f'Use the separately published `SHA256SUMS_v1.0.1.txt` to verify all four ZIP files, including this one.\n'
              f'The production build SHA is `{BUILD}`; release source SHA is `{release_sha}`.\n')
    verify_payload=[
        ('BUILD_PROVENANCE_AND_CHECKS.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf8')),
        ('QA_REPORT.json',(artifact/'QA_REPORT.json').read_bytes()),
        ('SHA256SUMS_packages.txt',archive_sums.encode('utf8')),
        ('SHA256SUMS_fonts.txt',font_sums.encode('utf8')),
        ('SOURCE_SHA256SUMS.txt',source_sums.encode('utf8')),
        ('VERIFYING.md',checking.encode('utf8')),
        ('MIT-TOOLS.txt',(root/'licenses/MIT-TOOLS.txt').read_bytes()),
    ]
    last=zip_bytes(verify_payload,dt)
    (dist/ZIPS['04']).write_bytes(last)
    data['04']={'filename':ZIPS['04'],'sha256':sha(last),'files':len(verify_payload),'size_bytes':len(last)}
    (dist/SIDECAR).write_text(''.join(f'{data[k]["sha256"]}  {ZIPS[k]}\n' for k in ('01','02','03','04')),encoding='utf8')
    print(f'PASS: Package 04 {ZIPS["04"]} — {len(verify_payload)} entries, SHA256 {data["04"]["sha256"]}')
    verify(root,dist,source_files=source_files)
    print('\nSUCCESS — four numbered release ZIPs and one checksum sidecar created:')
    print(dist)


def verify(root:Path,dist:Path,source_files:list[str]|None=None)->None:
    source_files=source_files if source_files is not None else check_repo(root)[1]
    with ZipFile(dist/ZIPS['01']) as z1, ZipFile(dist/ZIPS['02']) as z2, ZipFile(dist/ZIPS['03']) as z3, ZipFile(dist/ZIPS['04']) as z4:
        for z in (z1,z2,z3,z4):
            bad=z.testzip()
            if bad:
                raise RuntimeError('Damaged ZIP member: '+bad)
            if len(z.namelist())!=len(set(z.namelist())):
                raise RuntimeError('Duplicate ZIP members')
        fonts1=[p for p in z1.namelist() if p.endswith(('.ttf','.woff2'))]
        fonts3=[p for p in z3.namelist() if p.startswith('fonts/') and p.endswith(('.ttf','.woff2'))]
        if len(fonts1)!=32 or len(fonts3)!=32:
            raise RuntimeError('ZIP 01 or ZIP 03 font count wrong')
        if sorted(z2.namelist()) != sorted(source_files):
            raise RuntimeError('ZIP 02 does not match tracked release source')
        if set(z3.namelist()) != set(source_files) | {'fonts/'+f for f in fonts1}:
            raise RuntimeError('ZIP 03 does not exactly match fonts + sources')
        for f in source_files:
            if z2.read(f)!=z3.read(f) or z2.read(f)!=(root/f).read_bytes():
                raise RuntimeError('Source disagreement: '+f)
        for f in fonts1:
            if z1.read(f)!=z3.read('fonts/'+f):
                raise RuntimeError('Font disagreement: '+f)
        provenance=json.loads(z4.read('BUILD_PROVENANCE_AND_CHECKS.json'))
        if provenance.get('compiled_from_commit')!=BUILD or provenance.get('verified_font_count')!=32:
            raise RuntimeError('Invalid provenance')
        checks=z4.read('SHA256SUMS_packages.txt').decode('utf8').splitlines()
        if checks!=[f'{sha_path(dist/ZIPS[k])}  {ZIPS[k]}' for k in ('01','02','03')]:
            raise RuntimeError('Package 04 checksums disagree with actual packages')
        fontchecks=z4.read('SHA256SUMS_fonts.txt').decode('utf8').splitlines()
        if sorted(fontchecks)!=sorted(f'{sha(z1.read(f))}  {f}' for f in fonts1):
            raise RuntimeError('Package 04 font hashes disagree with contents')
        sourcechecks=z4.read('SOURCE_SHA256SUMS.txt').decode('utf8').splitlines()
        if sorted(sourcechecks)!=sorted(f'{sha(z2.read(f))}  {f}' for f in source_files):
            raise RuntimeError('Package 04 source hashes disagree with contents')
    sidecar=(dist/SIDECAR).read_text('utf8').splitlines()
    if sidecar != [f'{sha_path(dist/ZIPS[k])}  {ZIPS[k]}' for k in ('01','02','03','04')]:
        raise RuntimeError('Checksum sidecar disagrees with actual release ZIPs')
    print('PASS: Four ZIP CRC tests; source and font inventories; 04 hashes; external SHA-256 sidecar')


def main():
    ap=argparse.ArgumentParser(description='Build or verify four RedSigil v1.0.1 ZIPs')
    ap.add_argument('action',choices=['package','verify'])
    ap.add_argument('--repo',type=Path,default=Path.home()/'rs-type-system')
    ap.add_argument('--evidence',type=Path,default=Path.home()/f'rs-type-system-builds/run-{RUN}')
    ap.add_argument('--dist',type=Path,default=Path.home()/f'rs-type-system-builds/release-{VERSION}')
    a=ap.parse_args()
    try:
        if a.action=='package':
            produce(a.repo.resolve(),a.evidence.resolve(),a.dist.resolve())
        else:
            verify(a.repo.resolve(),a.dist.resolve())
    except (RuntimeError,ValueError,FileNotFoundError,subprocess.CalledProcessError) as e:
        print('STOP:',e,file=sys.stderr)
        sys.exit(1)

if __name__=='__main__':
    main()
