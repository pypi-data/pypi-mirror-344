import subprocess
import os
import graphviz
import re
from graphviz.exceptions import (
    ExecutableNotFound,
)  # recommended for specific error handling
import glob
from enum import Enum
from typing import Optional

from kieker.tools.command_builder import CommandBuilder
from IPython.display import display, IFrame
from pypdf import PdfWriter


class AnalysisType(Enum):
    AACTREE = ("--plot-Aggregated-Assembly-Call-Tree", None)
    ADCTREE = ("--plot-Aggregated-Deployment-Call-Tree", None)
    ACDGRAPH = ("--plot-Assembly-Component-Dependency-Graph", "none")
    AODGRAPH = ("--plot-Assembly-Operation-Dependency-Graph", "none")
    ASDIAGRAMS = ("--plot-Assembly-Sequence-Diagrams", None)
    CTREES = ("--plot-Call-Trees", None)
    CDGRAPH = ("--plot-Container-Dependency-Graph", None)
    DCDGRAPH = ("--plot-Deployment-Component-Dependency-Graph", "none")
    DODGRAPH = ("--plot-Deployment-Operation-Dependency-Graph", "none")
    DSDIAGRAMS = ("--plot-Deployment-Sequence-Diagrams", None)

    def __init__(self, command, default_param):
        self.command = command
        self.default_param = default_param

    def get_command(self, custom_param=None):
        param = custom_param if custom_param is not None else self.default_param
        return f"{self.command} {param}" if param else self.command


class GraphicType(Enum):
    PDF = "pdf"
    PNG = "png"
    SVG = "svg"


class TA:

    # config for trace analysis path
    trace_analysis_path = "~/Hackathon/trace-analysis-2.0.2/bin/trace-analysis"

    @staticmethod
    def set_trace_analysis_path(path: str):
        TA.trace_analysis_path = path

    @staticmethod
    def get_trace_analysis_path() -> str:
        return TA.trace_analysis_path

    @staticmethod
    def draw(
        analysis_type: AnalysisType,
        graphic_type: GraphicType,
        input_dir: str,
        output_dir: str,
        limit: Optional[int] = None,
        file_range: Optional[range] = None,
    ):
        """
        Executes the appropriate trace analysis method based on the given type.

        :param analysis_type: The type of analysis (AnalysisType Enum)
        :param graphic_type: The output graphic format (GraphicType Enum)
        :param input_dir: The directory containing Kieker logs
        :param output_dir: The target directory for the output
        :param limit: Maximum number of files to process
        :param file_range: Range of files to process (e.g., range(1, 5))
        """

        if limit is not None and limit <= 0:
            raise ValueError("Limit must be a positive integer or None.")
        if file_range is not None and (
            file_range.start < 1 or file_range.stop <= file_range.start
        ):
            raise ValueError(
                "Invalid range specified. Ensure start >= 1 and stop > start."
            )

        TA.analysis(
            analysis_type, graphic_type, input_dir, output_dir, limit, file_range
        )

        file_path = f"{output_dir}/output.{graphic_type.value}"
        if os.path.exists(file_path):
            frame = IFrame(file_path, width=600, height=300)
            display(frame)
        else:
            print(f"Error: File {file_path} could not be found.")

    @staticmethod
    def analysis(
        analysis_type: AnalysisType,
        graphic_type: GraphicType,
        input_dir: str,
        output_dir: str,
        limit: Optional[int] = None,
        file_range: Optional[range] = None,
    ):
        os.makedirs(output_dir, exist_ok=True)
        command = (
            CommandBuilder()
            .add(f"{TA.get_trace_analysis_path()}")
            .add(f"--inputdirs {input_dir}")
            .add(f"--outputdir {output_dir}")
            .add(f"{analysis_type.get_command()}")
            .to_string()
        )
        TA.run_command(command)
        file_name = f"{TA.extract_name(analysis_type.value[0])}"
        if os.path.isfile(f"{output_dir}/{file_name}.dot"):
            TA.dot_file_to_graphic_type(file_name, graphic_type, output_dir)
        elif glob.glob(os.path.join(output_dir, f"{file_name}-*.dot")):
            pdf_file_paths = TA.dot_files_to_pdf(
                file_name, output_dir, limit, file_range
            )
            TA.merge_pdf_files(pdf_file_paths, output_dir)
        elif glob.glob(os.path.join(output_dir, f"{file_name}-*.pic")):
            pdf_file_paths = TA.pic_files_to_pdf(
                file_name, output_dir, limit, file_range
            )
            TA.merge_pdf_files(pdf_file_paths, output_dir)
        else:
            raise FileNotFoundError(
                f"file {output_dir}/{file_name}.dot, {output_dir}/{file_name}-1.dot and {output_dir}/{file_name}-1.pic do not exist!"
            )

    @staticmethod
    def dot_file_to_graphic_type(
        file_name_base: str, graphic_type: GraphicType, output_dir: str
    ):
        """Converts a single .dot file with graphviz."""
        input_dot_path = os.path.join(output_dir, f"{file_name_base}.dot")
        output_path_with_ext = os.path.join(output_dir, f"output.{graphic_type.value}")

        try:
            graphviz.render(
                engine="dot",
                format=graphic_type.value,
                filepath=input_dot_path,
                outfile=output_path_with_ext,
            )

            if not os.path.exists(output_path_with_ext):
                print(
                    f"Warning: graphviz.render did not report an error, but the file {output_path_with_ext} was not found."
                )

        except ExecutableNotFound:
            print(
                f"ERROR: 'dot' executable not found. Is Graphviz correctly installed and in the system PATH?"
            )
            raise
        except Exception as e:
            print(f"ERROR converting {input_dot_path} with graphviz: {e}")
            raise

    @staticmethod
    def dot_files_to_pdf(
        file_name_base: str,
        output_dir: str,
        limit: Optional[int] = None,
        file_range: Optional[range] = None,
    ):
        dot_file_paths = glob.glob(os.path.join(output_dir, f"{file_name_base}-*.dot"))
        dot_file_paths.sort(key=TA.natural_sort_key)

        dot_file_paths_in_range = []

        if file_range is None:
            dot_file_paths_in_range = dot_file_paths
        else:
            dot_file_paths_in_range = [
                dot_file_path
                for dot_file_path in dot_file_paths
                if int(dot_file_path.split("-")[-1].split(".")[0]) in file_range
            ]

        pdf_file_paths = []

        counter = 1
        for dot_file_path in dot_file_paths_in_range:
            if limit is not None and counter > limit:
                break

            output_pdf_path = os.path.splitext(dot_file_path)[0] + ".pdf"

            try:
                graphviz.render(
                    engine="dot",
                    format="pdf",
                    filepath=dot_file_path,
                    outfile=output_pdf_path,
                )

                if os.path.exists(output_pdf_path):
                    pdf_file_paths.append(output_pdf_path)
                else:
                    print(
                        f"Warning: graphviz.render did not report an error, but the file {output_pdf_path} was not found."
                    )

            except ExecutableNotFound:
                print(
                    f"ERROR: 'dot' executable not found. Is Graphviz correctly installed and in the system PATH?"
                )
                raise
            except Exception as e:
                print(f"ERROR converting {dot_file_path} with graphviz: {e}")
                break

            counter += 1

        return pdf_file_paths

    @staticmethod
    def pic_files_to_pdf(
        file_name_base: str,
        output_dir: str,
        limit: Optional[int] = None,
        file_range: Optional[range] = None,
    ):
        pic_file_paths = glob.glob(os.path.join(output_dir, f"{file_name_base}-*.pic"))
        pic_file_paths.sort(key=TA.natural_sort_key)

        pic_file_paths_in_range = []

        if file_range is None:
            pic_file_paths_in_range = pic_file_paths
        else:
            pic_file_paths_in_range = [
                pic_file_path
                for pic_file_path in pic_file_paths
                if int(pic_file_path.split("-")[-1].split(".")[0]) in file_range
            ]

        pdf_file_paths = []
        counter = 1

        for pic_file_path in pic_file_paths_in_range:
            if limit is not None and counter > limit:
                break

            base_name = os.path.splitext(pic_file_path)[0]
            ps_file_path = f"{base_name}.ps"
            output_pdf_path = f"{base_name}.pdf"

            # execute pic2plot and ps2pdf
            command = (
                CommandBuilder()
                .add(f"pic2plot -T ps {pic_file_path} > {ps_file_path} &&")
                .add(f"ps2pdf {ps_file_path} {output_pdf_path}")
                .to_string()
            )
            TA.run_command(command)

            if os.path.exists(output_pdf_path):
                pdf_file_paths.append(output_pdf_path)

            counter += 1

        return pdf_file_paths

    @staticmethod
    def merge_pdf_files(pdf_file_paths, output_dir: str):
        writer = PdfWriter()
        for pdf in pdf_file_paths:
            writer.append(pdf)

        output_file_name = "output.pdf"
        writer.write(os.path.join(output_dir, output_file_name))
        writer.close()

    @staticmethod
    def extract_name(command: str) -> str:
        parts = command.replace("--plot-", "").split("-")
        name = parts[0].lower() + "".join(word.capitalize() for word in parts[1:])

        # Important: if the name ends with a 's' remove it for the file name purpose
        if name.endswith("s"):
            name = name[:-1]

        return name

    @staticmethod
    def run_command(command: str):
        try:
            subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    @staticmethod
    def natural_sort_key(s):
        # split in text/number blocks and converts numbers to int
        return [
            int(block) if block.isdigit() else block.lower()
            for block in re.split(r"(\d+)", s)
        ]
