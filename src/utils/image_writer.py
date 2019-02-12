class ImageWriter(object):
    def write(self, args):
        print("writing")
        for i in args:
            print(i, 'flow', i.flow)
