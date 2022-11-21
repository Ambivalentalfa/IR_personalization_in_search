
file="Qleft.txt"
def ret_q(file):
    q_dict={}
    with open(file) as f:
        for line in f:
            if line.startswith(">"):
                header=line.strip(">").strip("\n")
                q_dict[header]=[]
            else:
                q_dict[header].append(line.strip("\n"))
    return q_dict

def main():
    q=ret_q(file)
    for k,v in q.items():
        print(k)

if __name__ == '__main__':
    main()


