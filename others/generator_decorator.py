def generate(func):
    def gen_func(s):
        for item in s:
            yield func(item)
    return gen_func


# Sample use
if __name__ == '__main__':
    import math

    @generate
    def gen_sqrt(lst):
        return math.sqrt(lst)

    for i in gen_sqrt(range(5)):
        print(i)
