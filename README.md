# scraping


## usage
```bash
# obtain data from target site.
python ./get.py

# post article
python ./post.py
```

## other
1. `./get.py` will not insert same article, it's verified by `date`.
1. after `post.py` , `save.json` will be updated for `posted=true` .
`posted=true` object will not post again.
