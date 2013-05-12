
import sys

text = '''Lorem  ipsum dolor  sit  amet, consectetur  adipiscing  elit. Aliquam  pharetra sem. In tristique, ligula vitae rutrum ultrices, libero odio aliquet augue, sit amet  pharetra massa  neque ornare  enim. Nunc  lorem libero,  condimentum sed, blandit quis, tincidunt in, nulla.  Proin nec tortor. Vivamus nisl. Suspendisse ac massa.  Aenean porta enim  in mauris.  Morbi vestibulum.  Etiam sollicitudin tristique nisi. Vivamus mattis. Morbi felis. Integer felis.'''

def justify (text, width):
    ''' '''
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    words = text.split(' ')
    lines = [[],]
    x = 0
    for word in words:
        if not word: continue
        if (x+len(word)+1) > (width+1):
            x = 0
            lines.append([])
        lines[-1].append(word)
        x += len(word)+1
    for j in range(len(lines)):
        line = lines[j]
        if j == (len(lines)-1) or len(lines) == 1:
            for i in range(len(line)):
                line[i] += ' '
        else:
            s = width -1 - sum(len(word) for word in line)
            if len(line) > 2:
                for i in range(s):
                    line[i % (len(line)-1)] += ' '
            elif len(line) == 2:
                line[0] += ' '*s
    text = ''
    for line in lines:
        for word in line:
            text += word
        text += '\n'
    return text

print justify(text, 60)
