#!/usr/bin/env python3
import argparse, json, os, tempfile, sys
from offline_help_inventory import all_classifications
from offline_help_capture import group_classifications, validate_image_ref, capture_entry, SubprocessRunner, compare_manifests
class DriftError(RuntimeError): pass

def parse_images(values, roles):
    images={}
    for value in values:
        if value.count("=") != 1: raise ValueError("image must be role=immutable_ref")
        role, image=value.split("=",1)
        if role not in roles or role in images: raise ValueError("unknown or duplicate image role")
        images[role]=validate_image_ref(image)
    if set(images) != roles: raise ValueError("missing image role")
    return images

def build(images, runner):
    commands, noncommands=group_classifications(all_classifications())
    entries=[]
    for group in commands:
        captured=capture_entry(group,images[group["runtime"]],runner)
        captured.update({"id":group["id"],"challenge_ids":group["challenge_ids"]})
        entries.append(captured)
    entries.extend(noncommands)
    return {"schema_version":1,"entries":sorted(entries,key=lambda item:item["id"] if "id" in item else item["challenge_id"])}

def atomic_write(path, data):
    directory=os.path.dirname(os.path.abspath(path)); fd,tmp=tempfile.mkstemp(dir=directory,prefix=".offline-help-",text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as out: json.dump(data,out,sort_keys=True,indent=2); out.write("\n")
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--image",action="append",required=True); parser.add_argument("--output",required=True); parser.add_argument("--baseline")
    args=parser.parse_args(argv); roles={row["runtime"] for row in all_classifications() if "argv" in row}; manifest=build(parse_images(args.image,roles),SubprocessRunner())
    if args.baseline:
        try:
            with open(args.baseline,encoding="utf-8") as source: baseline=json.load(source)
            differences=compare_manifests(manifest,baseline)
        except (OSError,json.JSONDecodeError,ValueError) as exc: raise DriftError("invalid baseline") from exc
        if differences:
            raise DriftError("offline help drift: "+", ".join(resource+":"+field for resource,field in differences))
    atomic_write(args.output,manifest); return 0
if __name__=="__main__": raise SystemExit(main())
