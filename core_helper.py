import youtube_dl.extractor


def get_youtubedl_type(url):
    extractors = youtube_dl.extractor.gen_extractors()

    extractor_name = None
    for extractor in extractors:
        if extractor.suitable(url) and extractors.IE_NAME != 'generic':
            extractor_name = str(extractors).split('.')[-1].split(' ')[0]

    return extractor_name
