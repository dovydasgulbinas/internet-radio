#!/usr/bin/python3

OUTPUT_FORMAT = '- \"{} -> {}\"\n'
DEFAULT_PL_FILE = 'radio-main.m3u'
DEFAULT_YAML_NAME = 'results.yaml'


def parse_pl_fromdisk(fname):
    file = open(fname, 'r')
    playlist = file.read()
    return playlist


def dump_str_todisk(fname, strdump):
    with open(fname, 'w') as f:
        f.write(strdump)


def prepare_pl(playlist_string):
    lines = playlist_string.splitlines()
    stripedlines = list(map(lambda x:x.strip(), lines))
    header = stripedlines[0]
    assert header == '#EXTM3U', 'This script only supports EXTM3U playlists'
    return stripedlines


def dump_yaml(playlist_body):
    result = ''
    body_lines = len(playlist_body)

    for i in range(body_lines - 1):
        line_1 = playlist_body[i]

        if line_1.startswith('#EXTINF'):
            title = line_1.split(',')[-1]

            url = None
            for j in range(i + 1, body_lines):

                line_2 = playlist_body[j]

                if line_2:
                    url = line_2[i]
                    result+=OUTPUT_FORMAT.format(title, line_2)
                    i = j + 1
                    break

    return result



if __name__== "__main__":
    raw_pl = parse_pl_fromdisk(DEFAULT_PL_FILE)
    cooked_pl = prepare_pl(raw_pl)
    result = dump_yaml(cooked_pl)
    print(result)
    dump_str_todisk(DEFAULT_YAML_NAME, result)
