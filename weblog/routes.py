def includeme(config):
    config.add_static_view("static", "static", cache_max_age=3600)

    config.add_route("home", "/")
    config.add_route("post", "/post/{url_kword}")
    config.add_route("tags", "/tags")
    config.add_route("tag_posts", "/tags/{name}")
    config.add_route("about", "/about")
    config.add_route("language", "/language")
    config.add_route("rss", "/rss")

    config.add_route("images", "/images")
    config.add_route("image_submit", "/image-submit")

    config.add_route("resource_img", "/resource/image/{img_name}")

    config.add_route("add", "/edit")
    config.add_route("edit", "/edit/{post_id}")

