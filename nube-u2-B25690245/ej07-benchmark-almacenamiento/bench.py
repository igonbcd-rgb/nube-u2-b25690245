import os, time, hashlib, statistics as st, boto3

s3 = boto3.client("s3", endpoint_url=os.getenv("S3_ENDPOINT")) # None = AWS
BUCKET = os.environ["BUCKET"]

def sha(b): return hashlib.sha256(b).hexdigest()

def medir(mb, reps=5):
    datos = os.urandom(mb * 1024 * 1024)
    subida, bajada, errores = [], [], 0
    for i in range(reps):
        k=f"bench/{mb}MB-{i}"
        t = time.perf_counter(); s3.put_object(Bucket=BUCKET, Key=k, Body=datos)
        subida.append(mb / (time.perf_counter() - t))
        t = time.perf_counter(); leido = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()
        bajada.append(mb / (time.perf_counter() - t))
        errores += sha(leido) != sha(datos)
        s3.delete_object(Bucket=BUCKET, Key=k)
    print(f"{mb:>4} MB subida {st.mean(subida):6.1f}+-{st.stdev(subida):4.1f} MB/s "
        f"bajada {st.mean(bajada):6.1f}+-{st.stdev(bajada):4.1f} MB/s errores={errores}")
for mb in (1, 10, 100):
    medir(mb)