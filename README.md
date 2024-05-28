
# Load Testing with ApacheBench (ab) and Siege

reference: https://github.com/rm77/progjar/tree/master/progjar5

### ApacheBench (ab)

  ```bash
  sudo apt-get update
  sudo apt-get install apache2-utils
  ```

  ```bash
  ab -n [number of requests] -c [concurrency level] [URL]

  ab -n 1000 -c 10 https://127.0.0.1:8443/
  ```

  ### Siege

```bash
  sudo apt-get update
  sudo apt-get install siege
  ```

```bash
siege -c [concurrent users] -r [number of repetitions] [URL]
```
```bash
siege -c 10 -r 100 --no-check-certificate https://127.0.0.1:8443/
```
