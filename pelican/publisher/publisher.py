import subprocess
import os
import sys
from ftplib import FTP, error_perm

from assets_post_processor import AssetPostProcessor
import publisher_config as config


class Publisher(object):

    def __init__(self, config, post_slug):
        print("> STARTING")
        self.config = config
        self.output_folder = self.config.OUTPUT_FOLDER
        self.output_path = "./{output_folder}/".format(output_folder=self.output_folder)
        self.post_slug = post_slug

    def build_site(self):
        print("> BUILDING SITE")
        subprocess.call(["pelican", "content", "-s", "publishconf.py"])

        return self

    def run_post_build_tasks(self):
        print("> RUNNING POST BUILD TASKS")
        post_processor = AssetPostProcessor(self.config)
        post_processor.create_duplicates(self.output_path)
        post_processor.copy_files("./themes/{theme_name}/root-files/".format(theme_name=self.config.THEME_FOLDER),
                                  self.output_path)
        post_processor.remove_files(self.output_path)
        post_processor.remove_folders(self.output_path)

        return self

    def upload_files_if_proceeds(self):
        return self.upload_modified_files() if self.post_slug else self

    # TODO: Split in smaller methods
    def upload_modified_files(self):
        print("> UPLOADING MODIFIED FILES")

        if not os.path.exists("{output_folder}/post/{post_slug}".format(output_folder=self.output_folder,
                                                                        post_slug=self.post_slug)):
            print("ERROR: POST {post_slug} NOT FOUND".format(post_slug=self.post_slug))
            sys.exit()

        with FTP(self.config.FTP_HOST) as ftp_client:
            print(
                ftp_client.login(self.config.FTP_USERNAME, self.config.FTP_PASSWORD)
            )
            ftp_client.set_pasv(self.config.FTP_PASIVE_MODE)
            ftp_client.cwd("/apps/kartones.net/{ftp_folder}/{output_folder}".format(
                           ftp_folder=self.config.FTP_FOLDER, output_folder=self.output_folder))

            for file in self.config.ALWAYS_MODIFIED_FILES:
                local_path = "{output_folder}/{filepath}".format(output_folder=self.output_folder, filepath=file)
                print("UPLOADING '{filepath}'".format(filepath=local_path), end=" : ")
                if os.path.exists(local_path):
                    print(
                        ftp_client.storbinary("STOR {filename}".format(filename=file), open(local_path, "rb"))
                    )
                else:
                    print("ERROR: FILE '{filepath}' NOT FOUND".format(filepath=local_path))
                    sys.exit()

            filename = "index.html"
            ftp_client.cwd("post")
            try:
                print(
                    ftp_client.mkd(self.post_slug),
                    end=" : "
                )
            except error_perm:
                print("FOLDER '{folder}' MAYBE EXISTS, UPDATING CONTENT".format(folder=self.post_slug), end=" : ")
            ftp_client.cwd(self.post_slug)
            local_path = "{output_folder}/post/{post_slug}/{filename}".format(output_folder=self.output_folder,
                                                                              post_slug=self.post_slug,
                                                                              filename=filename)
            if os.path.exists(local_path):
                print(
                    ftp_client.storbinary("STOR {filename}".format(filename=filename), open(local_path, "rb"))
                )
            else:
                print("ERROR: FILE '{filepath}' NOT FOUND".format(filepath=local_path))
                sys.exit()

        print("URL: {base_url}post/{post_slug}/".format(base_url=self.config.WEBSITE_BASE_URL,
                                                        post_slug=self.post_slug))

        return self


def main(config):
    if len(sys.argv) != 2:
        post_slug = None
    else:
        post_slug = sys.argv[1]
    if len(sys.argv) > 2:
        print("USAGE: publisher.py [post-slug]")

    publisher = Publisher(config, post_slug)
    publisher.build_site() \
             .run_post_build_tasks() \
             .upload_files_if_proceeds()


if __name__ == '__main__':
    main(config)
