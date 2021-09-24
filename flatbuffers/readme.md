# flatbuffers for transferring animation frame information

```l
snap install flatc

flatc --python -o src flatbuffers/csa.fbs
git checkout HEAD -- src/casymda/__init__.py # (replacement of existing file avoidable?)

flatc --js -o src/casymda/visualization/web_server flatbuffers/csa.fbs
```
