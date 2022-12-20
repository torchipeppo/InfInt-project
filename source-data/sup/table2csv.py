import re

buf=""

with open("country-codes.xml", "r") as filein:
    with open("a.csv", "w") as fileout:
        for line in filein:
            # start blastin
            line = re.sub("</?table>", "", line)
            line = re.sub("</?thead>", "", line)
            line = re.sub("</?tbody>", "", line)
            line = re.sub("(\n|\t)+", "", line)

            # more careful
            line = re.sub("<tr>", "", line)
            line = re.sub("<th>", '"', line)
            line = re.sub("<td>", '"', line)

            # interesting
            line = re.sub("</tr>", "\n", line)
            line = re.sub("</th>", '",', line)
            line = re.sub("</td>", '",', line)

            buf += line

            while "\n" in buf:
                to_write, the_rest = buf.split("\n", maxsplit=1)
                to_write += "\n"
                to_write = re.sub(",+\n", "\n", to_write)

                fileout.write(to_write)

                buf = the_rest
