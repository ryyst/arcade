import glob
import re

fn_signature_w_docstring_regexp = re.compile(
    r"""
    (?P<fn_signature>
        (?P<fn_signature_before>
            def \s+
            (?P<fn_name> \S+ )              # Function name
            \( .*? \)                       # Parameter list
        )
        (?P<rtype_anno>                     # Return type annotation
            \s* -> \s*
            (?P<rtype_anno_type> .{1,300}? )
        )?
        :
    )
    [\r?\n\s]+
    (?P<docstring>
        \"\"\"                      # Docstring start
        (?P<docstring_body> .*? )
        \"\"\"                          # Docstring end
    )
    """,
    re.X | re.DOTALL)
docstring_regexp = re.compile(
    r"""
    (?P<docstring>
        \"\"\"                      # Docstring start
        (?P<docstring_body> .*? )
        \"\"\"                          # Docstring end
    )
    """,
    re.X | re.DOTALL)
docstring_rtype_regexp = re.compile(
    r"""
        \ +
        :rtype: \s* (?P<rtype> .*? ) \r?\n
    """,
    re.X | re.DOTALL)
docstring_return_regexp = re.compile(
    r"""
        (?P<indentation> \ + )
        :(return|returns|Returns):
        \s*
        (?P<description> .*? )
        \r?\n
    """,
    re.X | re.DOTALL)

count = 0
for file in [*glob.glob('arcade/*.py'), *glob.glob('arcade/**/*.py')]:
    with open(file, "r", newline='\n') as f:
        content = f.read()
    pos = 0
    while True:
        match = docstring_regexp.search(content, pos=pos)
        if match:
            # offset = 0
            match2 = docstring_return_regexp.search(match.group('docstring'))
            if match2:
                # Replace :return:
                range = match.start() + match2.start(), match.start() + match2.end()
                # offset -= range[1] - range[0]
                if match2.group('description'):
                    insert = f"{match2.group('indentation')}Returns:\n{match2.group('indentation')}    {match2.group('description')}\n"
                else:
                    insert = ''
                content = content[:range[0]] + insert + content[range[1]:]
                # pos = match.end('fn_signature_before')
                # content = content[:pos] + insert + content[pos:]
                # offset += len(insert)
            else:
                pos = match.end()
            # pos = match.end() + offset
        else:
            break
    with open(file, "w", newline='\n') as f:
        f.write(content)
print(count)