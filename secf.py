import re
def load(filename):
    section_dict={}
    with open(filename) as f:
        section_list=re.split('\\n\\n\\n+',f.read())
        for section in section_list:
            lines=section.strip('\n').split('\n')
            section_dict[lines[0]]=lines[2:]
    return section_dict

def save(sections,filename):
    try:
        f=open(filename,'w')
        count=1
        length=len(sections)
        for title,lines in sections.items():
            f.write(title+'\n')
            f.write('='*len(title)+'\n')
            for line in lines:
                f.write(line+'\n')
            if(count<length):
                f.write('\n\n')
            count+=1
        f.close()
    except:
        return False
    return True