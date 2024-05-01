import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import os

slidepaths = [
"Slide0.svg",
"motivation-1.svg",
"motivation-2.svg",
"motivation-3.svg",
"Bug-Finding-Techniques.svg",
"Fuzzing_Intro.svg",




"fuzzing-diagram.svg",
"thesis-statement.svg",
"rqs.svg",
"outline.svg",


"morphuzz-motivation.svg",
"Slide2.svg",
"Slide3_animated.svg",
"Slide4.svg",


"paper1.svg",
"Slide6_lens_animated.svg",
"Slide7.svg",
"Slide8.svg",

"Slide10_Results.svg",
"Slide11_Bugs.svg",
"Slide12_Upstream.svg",

"Slide13_MFConclusion.svg",


"paper3.svg",

"Blackbox.svg",
"Hp-Approach.svg",
"Hp-SysDiag.svg",
"Hp-Step1.svg",
"Hp-Step2.svg",
"Hp-Step3.svg",
"Hp-Results.svg",
"Hp-Bugs.svg",
"Hp-Conclusion.svg",

"paper2.svg",



"Slide4_syscalls.svg",
"Slide5_grammar.svg",
"Slide8_system_diagram.svg",
"Slide7_reexaminev2.svg",
"Slide9_NG-Agent.svg",
"Kernel_Results.svg",
"FuzzNG-Conclusion.svg",
"map.svg",
"rqs-revisited.svg",
"thesis-revisited.svg",
"bonus1.svg",
"bonus2.svg",
"Related_Work.svg",
"thanks.svg",
"fs.svg",

"Slide5_prior_work.svg",
"Grammars_Vdevs.svg",
"Slide9.svg",
"Slide12_Upstream.svg",
]

label = "{http://www.inkscape.org/namespaces/inkscape}label"

frames = []
framen = 0
sliden = 0
for path in slidepaths:
    layers = defaultdict(list)
    ignores = defaultdict(list)
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root.iter():
        _, _, tag = child.tag.rpartition('}')
        if tag == "g" and label in child.attrib and child.attrib[label].split(" ")[0].isnumeric():
            #print(child.attrib[label])
            n = int(child.attrib[label].split(" ")[0])
            layers[n].append(child)
            matches = re.findall('#RM\{(.*?)\}', child.attrib[label])
            for m in matches:
                ignores[n].append(m)
    if len(layers) == 0:
        layers[0] = []
    for n in sorted(layers.keys()):
        print("=== {}: {} ===".format(framen, n))
        for nn in sorted(layers.keys()):
            if nn > n:
                for layer in layers[nn]:
                    layer.set("style", "display:none")
                    print("{} not visible".format(layer.attrib[label]))
            else:
                for layer in layers[nn]:
                    layer.set("style", "display:visible")
                    for nnn in ignores:
                        if nnn <= n:
                            for ign in ignores[nnn]:
                                if ign in layer.attrib[label] and ign+"}" not in layer.attrib[label]:
                                    layer.set("style", "display:none")
                    if "visible" in layer.get("style"):
                            print("{} visible".format(layer.attrib[label]))
                    else:
                        print("{} invisible".format(layer.attrib[label]))

        frame = "/tmp/slides/{}.svg".format(framen)
        tree.write(frame)
        os.system('sed -i "s/>(p)/>{}/" {}'.format(sliden, frame))
        frames.append("/tmp/slides/{}.pdf".format(framen))
        os.system('/home/alxndr/Downloads/Inkscape-091e20e-x86_64.AppImage {} --export-type=pdf --export-filename={}'.format(frame, frames[-1]))
        framen +=1
    sliden +=1
