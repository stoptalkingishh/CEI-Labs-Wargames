"""Deterministic offline help capture; runner injection keeps tests Docker-free."""
import hashlib, re, subprocess
from urllib.parse import urlsplit, urlunsplit
URL=re.compile(r"<?https?://[^\s<>\"']+>?")
IMAGE_REF = re.compile(r"^[^\s@]+@sha256:[0-9a-f]{64}$")
MAX_STREAM_BYTES = 256 * 1024
class CaptureError(RuntimeError): pass

def normalize_url(candidate):
    if re.search(r"[\x00-\x1f\x7f]", candidate): raise CaptureError("invalid URL")
    value = candidate.strip().strip("<>")
    value = value.rstrip(".,;")
    while value and value[-1] in ")]}":
        opener = {')':'(', ']':'[', '}':'{'}[value[-1]]
        if value.count(value[-1]) > value.count(opener): value = value[:-1]
        else: break
    if re.search(r"%(?![0-9A-Fa-f]{2})", value): raise CaptureError("invalid URL")
    try: parsed = urlsplit(value)
    except ValueError as exc: raise CaptureError("invalid URL") from exc
    if parsed.scheme.lower() not in ("http","https") or parsed.username or parsed.password or not parsed.hostname: raise CaptureError("invalid URL")
    try: port = parsed.port
    except ValueError as exc: raise CaptureError("invalid URL") from exc
    scheme, host = parsed.scheme.lower(), parsed.hostname.lower()
    netloc = host if port is None or (scheme == "http" and port == 80) or (scheme == "https" and port == 443) else host + ":" + str(port)
    return urlunsplit((scheme, netloc, parsed.path or "/", parsed.query, parsed.fragment))

class SubprocessRunner:
    def __call__(self, args):
        try:
            result = subprocess.run(args, capture_output=True, timeout=5, check=False)
        except subprocess.TimeoutExpired as exc:
            raise CaptureError("capture timed out") from exc
        except OSError as exc:
            raise CaptureError("capture launch failed") from exc
        stdout, stderr = result.stdout or b"", result.stderr or b""
        if len(stdout) > MAX_STREAM_BYTES or len(stderr) > MAX_STREAM_BYTES:
            raise CaptureError("capture output exceeded limit")
        return {"stdout": stdout.decode("utf-8", "replace"), "stderr": stderr.decode("utf-8", "replace"), "exit_code": result.returncode}

def validate_image_ref(image):
    if type(image) is not str or not IMAGE_REF.fullmatch(image): raise ValueError("immutable image digest required")
    return image

def docker_command(image, argv, entrypoint=None):
    validate_image_ref(image)
    if not isinstance(argv, (list, tuple)) or not argv or any(type(arg) is not str or not arg or "\0" in arg for arg in argv): raise ValueError("invalid argv")
    ep = entrypoint or argv[0]
    if type(ep) is not str or not ep or "\0" in ep: raise ValueError("invalid entrypoint")
    return ["docker","run","--rm","--network","none","--read-only","--cap-drop","ALL","--security-opt","no-new-privileges","--pids-limit","64","--memory","128m","--cpus","0.5","--user","65534:65534","-e","LC_ALL=C","-e","LANG=C","-e","TERM=dumb","--entrypoint",ep,image,*argv[1:]]
def capture(entry, runner):
    image=entry["image"]
    result=runner(docker_command(image, entry["argv"]))
    if result.get("truncated"): raise ValueError("capture truncated")
    stdout,stderr=result["stdout"],result["stderr"]
    urls=[]
    for value in (stdout,stderr):
        for url in URL.findall(value):
            if len(url) > 2048: raise CaptureError("URL exceeds limit")
            normalized = normalize_url(url)
            if len(normalized) > 2048: raise CaptureError("URL exceeds limit")
            if normalized not in urls:
                urls.append(normalized)
                if len(urls) > 20: raise CaptureError("too many URLs")
    return {"id":entry["id"],"hint_argv":entry["argv"],"runtime":entry["runtime"],"image":image,"exit_code":result["exit_code"],"stdout_sha256":hashlib.sha256(stdout.encode()).hexdigest(),"stderr_sha256":hashlib.sha256(stderr.encode()).hexdigest(),"printed_urls":urls}

def capture_entry(entry, image, runner):
    argv, package = entry["argv"], entry["package"]
    def probe(command):
        result = runner(docker_command(image, command, entrypoint=command[0]))
        value = result["stdout"].strip()
        if result["exit_code"] != 0 or result["stderr"] or not value or "\n" in value: raise CaptureError("metadata probe failed")
        return value
    executable = probe(["/usr/bin/which", argv[0]])
    if not executable.startswith("/") or any(ch.isspace() for ch in executable): raise CaptureError("invalid executable path")
    version = probe(["/usr/bin/dpkg-query", "-W", "-f=${Version}", package])
    if not re.fullmatch(r"[A-Za-z0-9.+:~_-]+", version): raise CaptureError("invalid package version")
    result = capture({"id":entry.get("id","capture"),"argv":argv,"runtime":entry["runtime"],"image":image}, runner)
    result.update({"executable_path":executable,"package":package,"package_version":version})
    return result

def group_classifications(rows):
    commands, noncommands = {}, []
    seen_ids = set()
    for row in rows:
        for challenge_id in row["challenge_ids"]:
            if challenge_id in seen_ids: raise ValueError("duplicate challenge classification")
            seen_ids.add(challenge_id)
        if "argv" not in row:
            noncommands.extend({"challenge_id": cid, "status": "not_applicable", "reason": row["not_applicable"]} for cid in row["challenge_ids"])
            continue
        key = (row["runtime"], tuple(row["argv"]), row["package"])
        commands.setdefault(key, []).extend(row["challenge_ids"])
    output=[]; ids=set()
    for (runtime, argv, package), challenge_ids in commands.items():
        digest=hashlib.sha256("\0".join(argv).encode()).hexdigest()[:10]
        resource_id=re.sub(r"[^a-z0-9-]","-",runtime.lower()+"-"+argv[0].lower()+"-"+digest)[:64]
        if resource_id in ids: raise ValueError("resource id collision")
        ids.add(resource_id); output.append({"id":resource_id,"runtime":runtime,"argv":list(argv),"package":package,"challenge_ids":sorted(challenge_ids)})
    return sorted(output,key=lambda row:row["id"]), sorted(noncommands,key=lambda row:row["challenge_id"])

def compare_manifests(current, baseline):
    fields=("challenge_ids","status","challenge_id","argv","runtime","package","image","executable_path","package_version","exit_code","stdout_sha256","stderr_sha256","printed_urls")
    def index(manifest):
        if not isinstance(manifest,dict) or manifest.get("schema_version") != 1 or not isinstance(manifest.get("entries"),list): raise ValueError("invalid manifest schema")
        result={}
        for entry in manifest["entries"]:
            resource=entry.get("id",entry.get("challenge_id"))
            if not isinstance(resource,str) or resource in result: raise ValueError("duplicate manifest resource")
            result[resource]=entry
        return result
    left,right=index(current),index(baseline); differences=[]
    for resource in sorted(set(left)|set(right)):
        if resource not in left: differences.append((resource,"removed")); continue
        if resource not in right: differences.append((resource,"added")); continue
        for field in fields:
            if left[resource].get(field) != right[resource].get(field): differences.append((resource,field))
    return differences
