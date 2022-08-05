import os
import sys

SPK_MAGIC_VALUE = 0x444F4DEF

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: %s <spk file name>" % sys.argv[0])
    exit(-1)
  if not os.path.isfile(sys.argv[1]):
    print("%s: cannot access '%s': No such file or directory" % (sys.argv[0], sys.argv[1]))
    exit(-1)
  with open(sys.argv[1], "rb") as fp:
    first_4_bytes: bytes = fp.read(4)
    as_int = int.from_bytes(first_4_bytes, byteorder="little")
    if as_int != SPK_MAGIC_VALUE:
      print("%s: cannot get SPK information from %s: Invalid SPK file" % (sys.argv[0], sys.argv[1]))
      print("Got magic %s expected %s" % (hex(as_int), hex(SPK_MAGIC_VALUE)))
      exit(-1)
    fp.seek(20, os.SEEK_SET)
    stack_val_bytes = fp.read(4)
    stack = int.from_bytes(stack_val_bytes, byteorder="little")

    sys.stderr.write("####################################\n")
    sys.stderr.write("## Used memory size: %4d [KByte] ##\n" % ((stack & 0x00ffffff) // 1024))
    sys.stderr.write("####################################\n")
