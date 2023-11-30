from tex_paper_toolkit import DefaultToolkit

# instantiate a toolkit object
tex = DefaultToolkit()

# manually add new TeX (constant) definitions (\\newcommand)
tex.newcommand("constantOne", 1)
# by default, invalid characters are omited from the TeX label,
# but we can force serialization of digits via their names
tex.newcommand("constant2", 2, spell_digits=True)

# add custom TeX strings that should be directly serialized
# (the label here is just to get a unique identifier for the toolkit)
tex.texstring("emph-msg", r"\emph{Emphasized text}")

# specify a custom serialization target for this particular string (could also be achieved by using different `Toolkit` instances)
tex.texstring(
    "other-file-string",
    r"\textbf{Text in a different file!}",
    to_file="tex_texstring_output.tex",
)

# serialize the saved contents to the given TeX file
tex.serialize(to_file="tex_output.tex")
