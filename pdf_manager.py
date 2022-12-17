import argparse
import glob
import logging
import os
from datetime import datetime

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


class PDFManager:
    def merge_pdf(self, filename, source, dest=None):
        logging.info("=====MERGE PDF WORKFLOW=====")
        logging.info(f"Gathering file from {source}")
        files = glob.glob(os.path.join(source, "*.pdf"))
        pdf_merger = PdfFileMerger()

        for file in files:
            logging.debug(f"Adding file {file}")
            pdf_merger.append(file)

        if dest:
            dest = self.create_dir(dest)
            filename = os.path.join(dest, filename)
        logging.info(f"Saving file: {filename}")
        pdf_merger.write(filename)
        pdf_merger.close()

    @staticmethod
    def create_dir(dir_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def split_pdf(self, fname, target_dir=None):
        logging.info("=====SPLIT PDF WORKFLOW====")
        logging.info(f"Filename: {fname}")
        if target_dir:
            logging.debug(f"Creating Directory {target_dir}")
            target_dir = self.create_dir(target_dir)
        with open(file=fname, mode="rb") as rfile:
            logging.debug(f"Reading the file: {fname}")
            pdf_reader = PdfFileReader(rfile)
            for index in range(0, pdf_reader.numPages):
                logging.debug(f"Accessing page: {index+1}")
                page_obj = pdf_reader.getPage(index)
                filename = fname
                if target_dir:
                    filename = os.path.join(target_dir, fname)
                    filename = filename.replace(".pdf", "")
                split_fname = f"{filename}_{index+1}.pdf"
                pdf_writer = PdfFileWriter()
                logging.debug(f"Adding page {index+1} for file {split_fname}")
                pdf_writer.addPage(page_obj)
                logging.debug(f"Writing the file: {split_fname}")
                with open(split_fname, "wb") as wfile:
                    pdf_writer.write(wfile)
                logging.info("Saved successfully")


def get_input():

    # initialize argument parser
    parser = argparse.ArgumentParser(
        description="Python PDF Manager",
        epilog="Now you can split and Merge PDFs from here. Hurray!!",
    )

    parser.add_argument(
        "-w",
        "--workflow",
        help="Workflow: available options SPLIT MERGE",
        type=str,
        action="store",
        required=True,
    )

    parser.add_argument(
        "-s", "--source", help="Source", type=str, action="store", required=True
    )

    parser.add_argument(
        "-t", "--dest", help="Destination", type=str, action="store", required=True
    )

    args = parser.parse_args()
    return args.workflow, args.source, args.dest


def main():
    workflow, source, dest = get_input()
    pdf = PDFManager()
    if workflow.lower() == "split":
        pdf.split_pdf(source, dest)
    elif workflow.lower() == "merge":
        filename = datetime.now().strftime("merge_%Y-%m-%dT%H-%M-%S.pdf")
        pdf.merge_pdf(filename, source, dest)


if __name__ == "__main__":
    main()
