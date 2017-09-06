###############################################################################
# Copyright (c) 2017 Ericsson
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
###############################################################################

#args: filename filename-out

# Parses the HTML of lcov output and adds SonarQube-style Overall code coverage metric

# Example html content
#<tr>
#    <td class="headerItem">Test:</td>
#    <td class="headerValue">Basic example ( <span style="font-size:80%;"><a href="descriptions.html">view descriptions</a></span> )</td>
#    <td></td>
#    <td class="headerItem">Lines:</td>
#    <td class="headerCovTableEntry">20</td>
#    <td class="headerCovTableEntry">22</td>
#    <td class="headerCovTableEntryHi">90.9 %</td>
#</tr>
#<tr>
#    <td class="headerItem">Date:</td>
#    <td class="headerValue">2016-12-20 14:12:28</td>
#    <td></td>
#    <td class="headerItem">Functions:</td>
#    <td class="headerCovTableEntry">3</td>
#    <td class="headerCovTableEntry">3</td>
#    <td class="headerCovTableEntryHi">100.0 %</td>
#</tr>
#<tr>
#    <td class="headerItem">Legend:</td>
#    <td class="headerValueLeg"> Rating:
#        <span class="coverLegendCovLo" title="Coverage rates below 75 % are classified as low">low: &lt; 75 %</span>
#        <span class="coverLegendCovMed" title="Coverage rates between 75 % and 90 % are classified as medium">medium: &gt;= 75 %</span>
#        <span class="coverLegendCovHi" title="Coverage rates of 90 % and more are classified as high">high: &gt;= 90 %</span>
#    </td>
#    <td></td>
#    <td class="headerItem">Branches:</td>
#    <td class="headerCovTableEntry">8</td>
#    <td class="headerCovTableEntry">10</td>
#    <td class="headerCovTableEntryMed">80.0 %</td>
#</tr>


import sys
import re
fileContent = open(sys.argv[1]).read()

LC = -1
EL = -1
C = -1
B = -1
matchObject = re.finditer(".*<td class=.*(Lines:)</td>.*\n.*<td.*>(.*)</td>.*\n.*<td.*>(.*)</td>.*\n.*<td.*>(\d+\.\d+).*</td>", fileContent)
lineCov = 1.1
for m in matchObject:
    LC = float(m.group(2))
    EL = float(m.group(3))

matchObject = re.finditer(".*<td class=.*(Branches:)</td>.*\n.*<td.*>(.*)</td>.*\n.*<td.*>(.*)</td>.*\n.*<td.*>(\d+\.\d+).*</td>", fileContent)
for m in matchObject:
    C = float(m.group(2))
    B = float(m.group(3))

if LC * EL * C * B < 0:
    print "Could not compute coverage, negative values obtained."
    sys.exit(1)

print "Coverage = (CT + CF + LC)/(2*B + EL)"
print "Coverage = (%s + %s)/(2*%s + %s)" % (C, LC, B, EL)
COVERAGE = (C + LC)/(2*B + EL)
FORMATTED_COVERAGE = ("{0:.1f}".format(COVERAGE*100))
print "Result: %s" % FORMATTED_COVERAGE

REPLACEMENT = ("<tr>\n<td class=\"headerItem\">SonarQube-style:</td>\n<td></td>\n<td></td>\n<td></td>\n<td></td>\n<td></td>\n<td class=\"headerCovTableEntry\">%s %%</td>\n</tr>\n\g<1>" % FORMATTED_COVERAGE)
fileContent = re.sub("(.*<tr>.*\n.*<td class=.*(Legend:)</td>.*)", REPLACEMENT, fileContent)

open(sys.argv[2], "w").write(fileContent)
