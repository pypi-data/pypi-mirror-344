import dill as pickle
import tempfile
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Any, List

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import nbbase


class NotebookWrapper:
    def __init__(
        self,
        notebookFile: str | Path,
        inputVariable: str | List[str] | None,
        outputVariable: str | List[str] | None,
        inputTag: str = "input",
        outputTag: str = "output",
        allowError: bool = False,
        interactive: bool = False,
        nbContext: Path | None = None,
        cleanOldGenerated: bool = True,
    ):
        """_summary_

        Args:
            notebookFile (str | Path): _description_
            inputVariable (str | List[str] | None): _description_
            outputVariable (str | List[str] | None): _description_
            inputTag (str, optional): Currently do nothing. Defaults to "input".
            outputTag (str, optional): _description_. Defaults to "output".
            allowError (bool, optional): _description_. Defaults to False.
            interactive (bool, optional): Reload notebook every run. Defaults to False.
        """

        self.notebookPath = Path(notebookFile)

        if inputVariable is None:
            inputVariable = []
        elif isinstance(inputVariable, str):
            inputVariable = [inputVariable]
        self.inputVariable = inputVariable

        self.outputVariable = outputVariable

        self.inputTag = inputTag

        self.allowError = allowError

        self.interactive = interactive

        self.cleanOldGenerated = cleanOldGenerated
        
        if not self.interactive:
            self._readNotebook()

        if nbContext is not None:
            self.nbContext = nbContext
        else:
            self.nbContext = self.notebookPath.parent

        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, *kwargs)

    def run(self, *args, **kwargs) -> Any | List[Any]:
        return self._process(*args, **kwargs)[1]

    def export(self, _outputNotebook: str | Path, *args, **kwargs) -> Any | List[Any]:
        if isinstance(_outputNotebook, str):
            _outputNotebook = Path(_outputNotebook)

        _outputNotebook.parent.mkdir(parents=True, exist_ok=True)

        variableMapping, res, resultNb = self._process(*args, **kwargs)

        # Add markdown cell noting injected variables
        mdText = "`functionize-notebook` has modified this notebook during execution. The following variables have been injected:\n\n"
        for variable, varValue in variableMapping.items():
            try:
                varStr = str(varValue)
            except Exception:
                varStr = "This variable could not be represent in text."
            mdText += f"- {variable}: {varStr}\n"

        mdCell = nbbase.new_markdown_cell(source=mdText)
        mdCell.metadata["generated-by"] = "functionize-notebook"
        resultNb.cells[self.inputIndex] = mdCell

        del resultNb.cells[self.outputIndex]

        with open(_outputNotebook, "w") as f:
            nbformat.write(resultNb, f)
            pass

        return res

    def _process(self, *args, **kwargs):
        if self.interactive:
            self._readNotebook()

        # map input
        variableMapping = dict(zip(self.inputVariable, args))
        variableMapping.update(kwargs)

        nb = self.nb

        if len(variableMapping) > 0:
            # add saving path for input
            inputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebookPath.stem,
                "input",
                datetime.now().__str__() + ".pkl",
            )
            inputPath.parent.mkdir(parents=True, exist_ok=True)

            # add input values
            inputPath.write_bytes(pickle.dumps(variableMapping))
            # wait for nb input file
            for _ in range(50):
                if inputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(inputPath.__str__() + " took too much time to write.")

            self._insertInputCell(nb, inputPath)

        if self.outputVariable is not None:
            # add saving path for output
            outputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebookPath.stem,
                "output",
                datetime.now().__str__() + ".pkl",
            )
            outputPath.parent.mkdir(parents=True, exist_ok=True)

            self._insertOutputCell(nb, outputPath)
            pass

        ep = ExecutePreprocessor(timeout=None, allow_errors=self.allowError)
        resultNb, _ = ep.preprocess(nb, {"metadata": {"path": self.nbContext}})

        if self.outputVariable is not None:
            # wait for nb output
            for _ in range(50):
                if outputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(outputPath.__str__() + " took too much time to write.")

            res = pickle.loads(outputPath.read_bytes())

            return variableMapping, res, resultNb
        else:
            return variableMapping, None, resultNb

    def _readNotebook(self):
        self.nb = nbformat.read(self.notebookPath, as_version=nbformat.NO_CONVERT)

        # clean old generated
        if self.cleanOldGenerated:
            self.nb.cells = [
                cell
                for cell in self.nb.cells
                if not (cell.metadata.get("generated-by") == "functionize-notebook")
            ]

        self.inputIndex = -1
        for i, cell in enumerate(self.nb.cells):
            if "tags" in cell.metadata and self.inputTag in cell.metadata["tags"]:
                self.inputIndex = i + 1
                break
            pass

        inCell = nbbase.new_code_cell(source="")
        self.nb.cells.insert(self.inputIndex, inCell)

        self.outputIndex = len(self.nb.cells)
        outCell = nbbase.new_code_cell(source="")
        self.nb.cells.append(outCell)

    def _insertInputCell(self, nb, inputPath: Path):
        newCell = nbbase.new_code_cell(
            source="""
                from pathlib import Path
                import dill as pickle
                
                inputVariables = pickle.loads(Path("%s").read_bytes())
                for key, value in inputVariables.items():
                    globals()[key] = value
                    pass
            """
            % inputPath
        )

        nb.cells[self.inputIndex] = newCell

    def _insertOutputCell(self, nb, outputPath: Path):
        if isinstance(self.outputVariable, List):
            requestVars = "[" + ",".join(self.outputVariable) + "]"
        else:
            requestVars = self.outputVariable
        newCell = nbbase.new_code_cell(
            source="""
                from pathlib import Path
                import dill as pickle
                
                outputVariable = %s
                Path("%s").write_bytes(pickle.dumps(outputVariable))
            """
            % (requestVars, outputPath)
        )

        nb.cells[self.outputIndex] = newCell
