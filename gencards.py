import random, string

def gencard():
    s = '011'
    for y in range(3):
        s = s + '-';
        for x in range(4):
            s = s + s.join(random.choice(string.ascii_uppercase +
                                         string.digits))
    return(s)

if __name__ == "__main__":
    f = open('cards.csv', 'w')
    for x in range(50000):
        card = gencard()
        f.write('{0},{1}\n'.format(card, '$5'))

    f.close()
