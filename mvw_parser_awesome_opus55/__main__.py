"""Source: github.com/yihui-dev/awesome-opus5-5-videos (data/videos.json).

Gives prompt + creator metadata + poster. Videos themselves live on Skillry
(see mvw-parser-skillry-opus55); the same slug is used as item id.
"""
import json

from mvw_core import Item, cli_args, fetch_text

SOURCE = "awesome-opus55"
URL = "https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json"


def main():
    args = cli_args(__doc__)
    videos = json.loads(fetch_text(URL))
    new = 0
    for i, v in enumerate(videos):
        if args.limit and i >= args.limit:
            break
        it = Item(SOURCE, v["slug"])
        new += it.is_new
        if v.get("prompt"):
            it.save_text("prompt.txt", v["prompt"])
        poster = v.get("poster_url")
        if poster and not args.no_media:
            ext = poster.rsplit(".", 1)[-1]
            it.download("poster." + ext, poster)
        it.save_meta(
            title=v["slug"],
            author=v.get("author"),
            author_url=v.get("author_url"),
            post_url=v.get("post_url"),
            source_url=v.get("skillry_url"),
            category=v.get("category"),
            tags=v.get("tech_tags", []),
            prompt_partial=v.get("prompt_partial"),
            published=v.get("added"),
        )
    print(f"{SOURCE}: {min(len(videos), args.limit or len(videos))} items, {new} new")


main()
