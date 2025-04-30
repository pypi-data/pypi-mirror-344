import functools
import os
from snipper.block_parsing import indent
import sys
import subprocess


def o_block_funlines(lines, art, output, all_lines=None):
    id = indent(lines[0])
    if not os.path.isdir(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    # art = name
    outf = output + ("_" + art if art is not None and art != "" else "") + ".txt"
    l2 = []
    # Only import sys if not top level import.
    if len([l for l in all_lines if l.rstrip() == 'import sys']) == 0:
        l2 += [id + "import sys"]

    l2 += [id + f"sys.stdout = open('{outf}', 'w')"]
    l2 += lines
    l2 += [indent(lines[-1]) + "sys.stdout.close()"]
    l2 += [indent(lines[-1]) + "sys.stdout = sys.__stdout__"]
    return l2
    pass

def run_o(lines, file, output,package_base_dir=None, verbose=True, show_output=False):
    # def block_fun(lines, start_extra, end_extra, art, output, **kwargs):
    #     id = indent(lines[0])
    #     outf = output + ("_" + art if art is not None else "") + ".txt"
    #     l2 = []
    #     l2 += [id + "import sys", id + f"sys.stdout = open('{outf}', 'w')"]
    #     l2 += lines
    #     l2 += [indent(lines[-1]) + "sys.stdout = sys.__stdout__"]
    #
    #
    #     return l2, None
    try:
        from snipper.block_parsing import block_split, block_join
        # args = {k: v for k, v in b['start_tag_args'].items() if len(k) > 0}
        # cutout.append(b['block'])
        # b['block'], dn = _block_fun(b['block'], start_extra=b['arg1'], end_extra=b['arg2'], **args, keep=keep)
        # # cutout += b['block']
        # # method = b['start_tag_args'].get('', 'remove')
        # # b['block'], dn = _block_fun(b['block'], start_extra=b['arg1'], end_extra=b['arg1'], **args, keep=keep)
        # lines = block_join(b)

        while True:
            b = block_split(lines, tag="#!o")
            if b is None:
                break
            # ex = b['name']
            # o_block_fun(b['block'], None, )
            l2 = o_block_funlines( b['block'], b['name'], output, all_lines=lines)
            art = b['name']
            output_file = output + ("_" + art if art is not None and art != "" else "") + ".txt"

            lines2 = b['first'] + l2 + b['last']
            lines = b['first'] + b['block'] + b['last']
            fp, ex = os.path.splitext(file)
            file_run = fp + "_RUN_OUTPUT_CAPTURE" + ex
            # lines = lines2
            if os.path.exists(file_run):
                print("file found mumble...")
            else:
                with open(file_run, 'w', encoding="utf-8") as f:
                    f.write("\n".join(lines2))

                python = sys.executable
                if package_base_dir is None:
                    cmd = f"cd {os.path.dirname(file_run)} && {python} {os.path.basename(file_run)}"
                else:
                    # cmd = f"cd {os.path.dirname(package_base_dir)} && {python} {os.path.basename(file_run)}"
                    rp = os.path.relpath(file_run, package_base_dir).replace("\\", "/").replace("/", ".")[:-3]
                    cmd = f"cd {package_base_dir} && {python} -m {rp}"

                if verbose:
                    print(cmd)
                    if show_output:
                        print("File that will be run contains:", file_run)
                        with open(file_run, 'r') as f:
                            print(f.read())
                s = subprocess.check_output(cmd, shell=True)
                if verbose:
                    # print("[snipper] Obtained output")
                    # print(s)

                    if os.path.isfile(output_file):
                        print("[snipper] Snipper generated output to file", output_file)
                        if show_output:

                            with open(output_file, 'r') as f:
                                print(f.read())
                            print(">> WAS THAT WHAT YOU EXPECTED???")
                    else:
                        print("[snipper] No output file produced which is quite odd. The terminal output is")
                        print(s)
                        print(f"[snipper] No output file produced: {output_file=}")
                os.remove(file_run)


        # lines2, didfind, extra, _ = block_process(lines, tag="#!o", block_fun=functools.partial(block_fun, output=output) )
    except Exception as e:
        print("Bad file: ", file)
        print("I was cutting the #!o tag")
        print("\n".join( lines) )
        raise(e)
