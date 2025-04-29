"""
Doc Generator
==============

An object that handles creating docs for labview projects.



"""
from pathlib import Path, PureWindowsPath
import lv_doc_tools.xml_adoc_conversion as xml2adoc
import subprocess
from sys import platform
import re
import time
import os


class Doc_Generator:
    """
    This class hqndles the generation of documents from LabView source files.
    It uses both antidoc and asciidoctor-pdf.
    It allows the users to include additional sources from the Caraya test output.

    :param config: a dictionary of configuration parameters.

    The config is a dictionary with the following fields:

    .. code:: python

        "PATHS": {
            "ROOT": "PATH_TO_PROJECT_FOLDER",
	    "LV_PROJ": "THE_PROJECT.lvproj",
	    "TESTS": "RELATIVE PATH TO TESTS",
	    "OUTPUT": "relative_path_to_output_folder",
	    "CARAYA": "Absolute Path_to_Caraya_toolkit",
	    "TEST_XML": "relative path to test xml output",
	    "DOC_SOURCE": "relative path to additional adoc files, e.g converted xml",
	    "ANTIDOC_CONFIG":"rel_path_to_antidoc.config"
        },
        "TEST_ITEMS": [list of test VIs],
        "EMAIL": "info@resonatesystems.com.au",
        "AUTHOR": "Resonate Systems",
        "PAGE_TITLE": "A string"

    """

    def __init__(self, config):
        """
        Constructor method, the following fields in config are required

        * 'ROOT'
        * 'LV_PROJ_PATH'
        *
        """
        try:
            self.add_config_paths(config["PATHS"])
            self.add_attributes(config)
        except Exception as e:
            print(f"Config error: {e}")
            raise
        # Set the head source file
        head_file = self.paths['lv_proj'].stem + ".adoc"
        self.head_file = self.paths['output'].joinpath(head_file)

    def add_config_paths(self, config):
        """
        Create Path() objects from the config paths dictionary.
        Set default values if items not present
        Raise error if mandatory items not present, e.g lv_proj_path

        """
        paths = {}
        self.root = Path(config["ROOT"]).resolve()

        if "LV_PROJ" in config.keys():
            paths['lv_proj'] = self.root.joinpath(Path(config["LV_PROJ"]))

        if "TESTS" in config.keys():
            # Where tests can be found relative to root
            paths['tests'] = self.root.joinpath(Path(config["TESTS"]))
        else:
            paths['tests'] = self.root.joinpath(Path("Tests"))

        if "OUTPUT" in config.keys():
            # OUTPUT pqth is where the build docs land, relative to root
            paths['output'] = self.root.joinpath(Path(config["OUTPUT"]))

        if "CARAYA" in config.keys():
            # Where teh carya CLI engine lives.
            paths['caraya'] = self.root.joinpath(Path(config["CARAYA"]))
        else:
            paths['caraya'] = PureWindowsPath(
                "C:\\Program Files\\National Instruments\\LabVIEW 2025\\vi.lib\\addons\\_JKI Toolkits\\Caraya\\CarayaCLIExecutionEngine.vi",
            )

        if "TEST_XML" in config.keys():
            # TEST_XML_PATH is where the caryaya test app saves xml output. Relative to output_path
            paths['test_xml'] = paths['tests'].joinpath(Path(config["TEST_XML"]))

        if "DOC_SOURCE" in config.keys():
            # DOC_SOURCE_PATH is where adoc files land, realtive to the root path.
            paths['doc_source'] = self.root.joinpath(Path(config["DOC_SOURCE"]))

        if "ANTIDOC_CONFIG_PATH" in config.keys():
            # The antidoc config file, as saved using the antidoc app, relative to root
            paths['antidoc_config'] = self.root.joinpath(
                Path(config["ANTIDOC_CONFIG_PATH"])
            )
        else:
            paths['antidoc_config'] = paths['lv_proj'].stem + ".config"
        self.paths = paths

    def add_attributes(self, config):
        """
        Handle non pathitems from the config.
        Set defaults if items are missing
        """
        if "AUTHOR" in config.keys():
            self.author = config["AUTHOR"]
        else:
            self.author = "Resonate Systems"

        if "EMAIL" in config.keys():
            self.email = config["EMAIL"]
        else:
            self.email = "info@resonatesystems.com.au"

        if "TITLE" in config.keys():
            self.title = config["TITLE"]
        else:
            self.title = f"Documentation For {config['PATHS']['LV_PROJ']}"

        if "TESTS" in config.keys():
            # Names of test vi's, relative to TESTS_PATH
            self.tests = [self.paths['tests'].joinpath(x) for x in config["TESTS"]]
        else:
            self.tests = []

        if "CONFLUENCE" in config.keys():
            self.confluence = config['CONFLUENCE']

    def make_antidoc_command(self):
        """
        Create the CLI command needed to run antidoc and crete build source files
        """
        gcli_command = [
            "g-cli",
            "--lv-ver",
            "2025",
            "antidoc",
            "--",
            "-addon",
            "lvproj",
            "-pp",
            f"'{self.paths['lv_proj']}'",
            "-t",
            self.title,
            "-out",
            f"'{(self.paths['output'])}'",
            "-e",
            self.email,
            "-a",
            self.author,
            "-configpath",
            f"'{self.root.joinpath(self.paths['antidoc_config'])}'",
        ]
        self.antidoc_command = gcli_command

    def make_ascii_doctor_command(self):
        """
        Create the  ascii doctor command to convert .adoc files to pdf
        """

        cmd = ["asciidoctor-pdf"]
        # cmd.append(f" -D '{self.paths['output']}'")
        # cmd += '' ADD OTHER ARGS HERE
        cmd.append(f"'{self.head_file}'")  # .replace('\\','/').replace('C:', '/c'))
        self.ascii_doctor_command = cmd

    def run_command(self, cmd):
        """
        Run a system command, this uses os.system
        :TODO: check behaviour again with subprocess()

        """

        if platform == "linux" or platform == "linux2" or platform == "darwin":
            # OS X or Linux
            print(cmd)
        elif platform == "win32":
            # Windows...
            try:
                # proc = subprocess.run(cmd) #, check=True)
                cmd_str = " ".join(cmd)
                print(f"\n\n{cmd_str}\n\n")
                os.system(cmd_str)

            except Exception as err:
                print("Error running CLI command")
                raise

    def tweak_adocs(self):
        """
        Alter the vanilla adocs generated by antidoc

        Currently it removes legal notices and wovalab in title, also sets TOC depth.
        """
        tmp_file = self.paths['output'].joinpath("tmp.adoc")
        # Remove the gratuitous wovalabs text
        #
        ptns = [
            "^Antidoc v[0-9.]+;(.*)",  # get the text after the antidoc statement
            "^:toclevels: (2)",  # get the toc level line
            "== Legal Information",  # get the start of legal info
        ]
        # read in head file
        with open(self.head_file, "r") as orig:
            with open(tmp_file, "w+") as new:
                for line in orig:
                    m = re.match("^Antidoc v[0-9.]+;(.*)", line)
                    if m:
                        new.write(m[1] + "\n")
                        continue
                    m = re.match("^:toclevels:", line)
                    if m:
                        new.write(":toclevels: 4\n")
                        continue
                    m = re.match("^== Legal Information", line)
                    if m:
                        break
                    else:
                        new.write(line)
        Path(tmp_file).replace(self.head_file)

    def add_sources(self, sources, header_text="\n== Appendix\n"):
        """
        Add include statments to head adoc file
        to include the sources

        Optionally allows a new section title.
        """
        print(f"Head File is {str(self.head_file)}")
        print(f"Added sources are: {sources}")
        with open(self.head_file, "a+") as fh:
            fh.write(header_text)
            for src in sources:
                fh.write(f"include::{str(src)}[leveloffset=+1]\n")

    def build_docs(self):
        """
        Based on config values build the docs
        1. Build adoc from LV proj - antidoc_command
        2. Convert XML test outputs to adoc
        3. Tweak adoc output to remove unwanted material and update style
        4. Add test report adoc content
        5. Generate required outputs,  PDF

        :TODO: Add some switching here to control what happens based on config flags
        """

        # . 1 Run the anti doc command - this yields adoc files in output_path along with Image and Include directory
        self.make_antidoc_command()
        try:
            self.run_command(self.antidoc_command)
        except Exception as err:
            print(self.antidoc_command)
            print(err)

        # 2. Convert XML in test output to adoc - yields adoc files in DOC_SOURCE_PATH
        if platform == "win32":
            # create dictionary of tests
            self.root.joinpath("temp_xml").mkdir(parents=True, exist_ok=True)
            tmp_dir = self.root.joinpath("temp_xml")
            out_file = self.paths['doc_source'].joinpath("test_results.adoc")
            out_file.parents[0].mkdir(parents=True, exist_ok=True)
            test_dicts = [
                {"test_name": f.stem, "xml_filepath": f}
                for f in self.paths['test_xml'].glob("*.xml")
            ]
            xml2adoc.parse_multiple_to_adoc(test_dicts, out_file, tmp_dir)
        else:
            print(f"xml to adoc\n{self.paths['test_xml']}\n{self.paths['doc_source']}")

        # 3. Tweak adoc source - Adjust head adoc file 
        self.tweak_adocs()

        # 4. Add in test report content from DOC_SOURCE_PATH
        sources = [x for x in self.paths['doc_source'].glob("*Test*.adoc")]
        self.add_sources(sources, header_text="")
        
        # 5. Run asciidoctor
        self.make_ascii_doctor_command()
        print(f"\n\nASCII DOC PDF: {self.ascii_doctor_command}\n\n")
        try:
            self.run_command(self.ascii_doctor_command)
        except Exception as err:
            print(self.ascii_doctor_command)
            print(err)

    def publish_to_confluence(self):
        """
        Push HTML output to confluence
        """
        for filename in os.listdir(self.paths['output']):
            if filename.endswith(".html"):
                html_file_path = os.path.join(self.paths['output'], filename)
                print(f"HTML file path is {html_file_path}")

                try:
                    with open(html_file_path, "r", encoding="utf-8") as file:
                        html_content = file.read()

                    # Check if the Confluence page exists
                    page_id = None
                    if confluence.page_exists(self.space_key, self.title):
                        existing_page = confluence.get_page_by_title(
                            self.space_key, self.title
                        )
                        if existing_page:
                            page_id = existing_page["id"]
                    else:
                        # Create a new page and get its ID
                        created_page = confluence.create_page(
                            space=self.space_key,
                            title=self.title,
                            body="Temporary content...",
                        )
                        page_id = created_page["id"]
                        print("New page created.")

                    # Upload images to Confluence & get their attachment URLs
                    image_urls = {}
                    for image_filename in os.listdir(self.image_dir):
                        if image_filename.lower().endswith(
                            (".png", ".jpg", ".jpeg", ".gif")
                        ):
                            image_path = os.path.join(self.image_dir, image_filename)

                            with open(image_path, "rb") as img_file:
                                response = confluence.attach_content(
                                    content=img_file.read(),
                                    name=image_filename,
                                    content_type="image/png"
                                    if image_filename.endswith(".png")
                                    else "image/jpeg",
                                    page_id=page_id,  # Attach image to the correct page
                                )
                            if response:
                                print(f"Uploaded {image_filename} successfully!")
                                # Confluence stores attachments in this format
                                image_urls[
                                    image_filename
                                ] = f'<ac:image><ri:attachment ri:filename="{image_filename}"/></ac:image>'
                            else:
                                print(f"Failed to upload {image_filename}")

                    # Replace local image paths in HTML with Confluence formatted image tags
                    for image_filename, image_tag in image_urls.items():
                        html_content = html_content.replace(
                            f'src="Images/{image_filename}"', image_tag
                        )
                        html_content = html_content.replace(
                            f'src="./Images/{image_filename}"', image_tag
                        )
                        html_content = re.sub(r'alt="[^"]*">', "", html_content)

                    # Update the Confluence page with modified HTML content
                    response = confluence.update_page(
                        page_id=page_id,
                        title=self.title,
                        body=html_content,
                        representation="storage",
                        full_width=True,
                    )

                    print("Page Updated Successfully!")

                except FileNotFoundError:
                    print(f"HTML file {filename} not found at {html_file_path}")

                except Exception as e:
                    print(f"Error processing {html_file_path}: {e}")
            if MAKE_PDF:
                if filename.endswith(".pdf"):
                    pdf_file_path = os.path.join(self.paths['output'], filename)
                    response = confluence.attach_file(
                        filename=pdf_file_path,
                        name="Hitachi Code review Doc.pdf",
                        content_type="aaplication/pdf",
                        page_id=page_id,
                    )
                    print("PDF file attached successfully")
