import re
import requests

class Page:
    def __init__(self, path: str):
        self.name = path.split('/')[-1]
        self.path = path
        self.contents = self.__get_contents()

    def __get_contents(self):
        with open(self.path, 'r') as f:
            return f.read()

    def do_replacements(self, replacements):
        self.replace_spotify()
        self.replace_twitter()
        self.replace_youtube()
    
    def replace_spotify(self):
        link_pattern = "https://open.spotify.com/(?:track|album|playlist|artist)/.{22}(?:\\?si=.{16})"
        pattern = "(<figure id=\".{36}\"><div class=\"source\"><a href=\"LINK_PATTERN\">LINK_PATTERN</a></div></figure>)"
        full_pattern = pattern.replace('LINK_PATTERN', link_pattern)

        template = "<iframe src=\"URL\" width=\"350px\" height=\"80px\" frameBorder=\"0\" allowtransparency=\"true\" allow=\"encrypted-media\"></iframe>"

        for match in re.findall(full_pattern, self.contents):
            filled_template = template\
                .replace('URL', re.findall(link_pattern, match)[0])

            self.contents = self.contents.replace(match, filled_template)

    def replace_twitter(self):
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-oembed
        link_pattern = "https?:\/\/twitter\.com\/(?:#!\/)?(?:\w+)\/status(?:es)?\/(?:\d+)"
        pattern = "(<figure id=\".{36}\"><div class=\"source\"><a href=\"LINK_PATTERN\">LINK_PATTERN</a></div></figure>)"
        full_pattern = pattern.replace('LINK_PATTERN', link_pattern)

        for match in re.findall(full_pattern, self.contents):
            tweet_url = re.findall(link_pattern, match)[0]
            r = requests.get(f'https://publish.twitter.com/oembed?url={tweet_url}')

            self.contents = self.contents.replace(match, r.json()['html'])

    def replace_youtube(self):
        link_pattern = '(?:(?:https?:)?\/\/)?(?:(?:www|m)\.)?(?:(?:youtube\.com|youtu.be))(?:\/(?:[\w\-]+\?v=|embed\/|v\/)?)(?:[\w\-]+)(?:\S+)?'
        pattern = "(<figure id=\".{36}\"><div class=\"source\"><a href=\"LINK_PATTERN\">LINK_PATTERN</a></div></figure>)"
        video_id_pattern = "watch\?v=(.{11})"
        full_pattern = pattern.replace('LINK_PATTERN', link_pattern)

        for match in re.findall(full_pattern, self.contents):
            print(match)
            template = f"""
                <iframe 
                    width="1061"
                    height="596"
                    src="https://www.youtube.com/embed/{re.findall(video_id_pattern, match)[0]}"
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            """

            self.contents = self.contents.replace(match, template)
