# bittorrent v2 merkle root hash py

get bittorrent v2 merkle root hash of file path

## demo

```
$ ./btrhsum.py <(dd if=/dev/urandom bs=1024 count=100 status=none)
f3aa652ef4373e7f19fcddd4cbe2c21dfc18641b9dabef6cacb177b89477eb3a

$ ./btrhsum.py -l <(dd if=/dev/urandom bs=1024 count=100 status=none)
fb06b32ccd979c891397f6917325353a778f48ef976b34530c128c755ed5dd24
7615361c09e55c2e475fc14f44cd56d5282dce868108173c76728fc7dea93091
92a35f91f7290dba4a1eb10520139727c921df194acca5cd8878fbf48594e550
aac3d430df2316a464b8ba6ac05418d24e58c726cf1d0d913131c5831a427908
b76d67d3e05c706d953876a5c7b03299ccbcc6b27d0e21d68226a48fd9320243
dff12e738d21b68b590bd91fb4966a0eed1216a5befc130ac11ef68005fd7591
8626c3a43543c71bd5267d7262b259710213acb3fdc398315ddcd6846d771fd1
```

### large input file

```
$ du -h opensubs.db
128G    opensubs.db

$ du -b opensubs.db
136812494848    opensubs.db

$ # how many leaf hashes?
$ expr 136812494848 / 1024 / 16
8350372

$ $(which time) -v btrhsum.py -a opensubs.db >opensubs.db.bt2h.hex
        User time (seconds): 3082.08
        System time (seconds): 463.50
        Percent of CPU this job got: 56%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 1:43:41
        Maximum resident set size (kbytes): 1266984

$ expr 1266984 / 1024
1237

$ # TODO why did this need 1.24GiB of RAM? all hashes have only 0.25GiB

$ wc -l opensubs.db.bt2h.hex
8350373 opensubs.db.bt2h.hex

$ du -h opensubs.db.bt2h.hex
518M    opensubs.db.bt2h.hex

$ # convert hex to binary. same result as "btrhsum.py -a -b"
$ cat opensubs.db.bt2h.hex | xxd -r -p >opensubs.db.bt2h

$ du -h opensubs.db.bt2h
255M    opensubs.db.bt2h

$ du -b opensubs.db.bt2h
267211936       opensubs.db.bt2h

$ expr 136812494848 / 267211936
511

$ # so all hashes are about 1/500 = 0.2% of the input file size

$ expr 128 \* 1024 / 1000 \* 2
262

$ # get hex hashes from binary hashes file

$ head -c$((1 * 32)) opensubs.db.bt2h | xxd -p -c32
5bc22db1cac8213887cc255f9a994e3f7b6aa236c0afa3be492425a1133a7342

$ tail -c$((1 * 32)) opensubs.db.bt2h | xxd -p -c32
406e5bb482777d3ae9ad1c9fd3569132d39eda525726ea5da637fba393bd2f34

$ # verify some hashes

$ n=3; for i in $(seq 0 $((n - 1))); do dd if=opensubs.db bs=$((16 * 1024)) count=1 skip=$i status=none | sha256sum -; done | cut -d' ' -f1
5bc22db1cac8213887cc255f9a994e3f7b6aa236c0afa3be492425a1133a7342
1b30b97f6053802062cfce5224ef4839d28725e6f5dd1796a559f53192acdded
84c506d6f3795f907dac603cc02f22b1949b3a1f222f6079f46650ad6b1f205a

$ head -n3 opensubs.db.bt2h.hex
5bc22db1cac8213887cc255f9a994e3f7b6aa236c0afa3be492425a1133a7342
1b30b97f6053802062cfce5224ef4839d28725e6f5dd1796a559f53192acdded
84c506d6f3795f907dac603cc02f22b1949b3a1f222f6079f46650ad6b1f205a
```
