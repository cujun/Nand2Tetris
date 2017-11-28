#
# Compile Jack source to VM
#

import tokens
import jackparser
from parsetree import *
import sys, os

# --------------------------------------------------------------------

binopmap = { "+" : "add",
             "-" : "sub",
             "*" : "call Math.multiply 2",
             "/" : "call Math.divide 2",
             "&" : "and",
             "|" : "or",
             ">" : "gt",
             "<" : "lt",
             "=" : "eq" }

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
  
# --------------------------------------------------------------------

class JackCompiler():
  def __init__(self, folder):
    self.folder = folder

  # ------------------------------------------------------------------
    
  def compile(self, jclass):
    "Compile one class."
    sys.stderr.write("Compiling %s ...\n" % jclass.name)
    self.out = open("%s/%s.vm" % (self.folder, jclass.name), "w")
    self.out.write("// class %s\n" % jclass.name)
    for sb in jclass.subroutines:
      self.out.write("// %s %s %s.%s\n" %
                     (sb.kind, sb.ret_type, jclass.name, sb.name))
      self.compile_subroutine(jclass, sb)
    self.out.close()

  def compile_subroutine(self, jclass, sb):
    self.out.write("function %s.%s %d\n" %
                   (jclass.name, sb.name, len(sb.locals)))
    if sb.kind == 'method':
      self.out.write("push argument 0\npop pointer 0\n")
    elif sb.kind == 'constructor':
      self.out.write("push constant {}\ncall Memory.alloc 1\npop pointer 0\n".format(len(jclass.fields)))
    for st in sb.statements:
      self.compile_statement(jclass, sb, st)

  def compile_statement(self, jclass, sb, st):
    if isinstance(st, LetStatement):
      self.compile_let(jclass, sb, st)
    if isinstance(st, CallExpression):
      self.compile_do(jclass, sb, st)
    if isinstance(st, IfStatement):
      self.compile_if(jclass, sb, st)
    if isinstance(st, WhileStatement):
      self.compile_while(jclass, sb, st)
    if isinstance(st, ReturnStatement):
      self.compile_return(jclass, sb, st)

  # ------------------------------------------------------------------

  #
  # In all compile_xxx methods, jclass is a JackClass object
  # describing the class containing the code being compiled, and
  # sb is a Subroutine object describing the function/method/constructor.
  # 

  # let is of type LetStatement
  def compile_let(self, jclass, sb, let):
    self.compile_expression(jclass, sb, let.expr)
    for idx, argument in enumerate(sb.arguments):
      if argument[0] == let.vname:
        lval = "argument {}".format(idx + (1 if sb.kind == 'method' else 0))
    for idx, local in enumerate(sb.locals):
      if local[0] == let.vname:
        lval = "local {}".format(idx)
    for idx, static in enumerate(jclass.statics):
      if static[0] == let.vname:
        lval = "static {}".format(idx)
    for idx, field in enumerate(jclass.fields):
      if field[0] == let.vname:
        lval = "this {}".format(idx)
    if let.index is None:
      self.out.write("pop {}\n".format(lval))
    else:
      self.out.write("push {}\n".format(lval))
      self.compile_expression(jclass, sb, let.index)
      self.out.write("add\npop pointer 1\npop that 0\n")

  # st is of type CallExpression
  def compile_do(self, jclass, sb, st):
    self.compile_call(jclass, sb, st)
    self.out.write("pop temp 0 // void\n")

  # ifst is of type IfStatement
  @static_vars(counter=0)
  def compile_if(self, jclass, sb, ifst):
    # list of needed labels
    label_basic = "{}.{}.IF{}".format(jclass.name.upper(), sb.name.upper(), JackCompiler.compile_if.counter)
    label_else, label_end = label_basic + "_ELSE", label_basic + "_END"
    JackCompiler.compile_if.counter += 1

    self.compile_expression(jclass, sb, ifst.expr)
    self.out.write("not\nif-goto {}\n".format(label_else))
    for statement in ifst.if_statements:
      self.compile_statement(jclass, sb, statement)
    self.out.write("goto {}\n".format(label_end))
    self.out.write("label {}\n".format(label_else))
    for statement in ifst.else_statements if ifst.else_statements is not None else []: # exceptional case
      self.compile_statement(jclass, sb, statement)
    self.out.write("label {}\n".format(label_end))

  # whilest is of type WhileStatement
  @static_vars(counter=0)
  def compile_while(self, jclass, sb, whilest):
    # list of needed labels
    label_basic = "{}.{}.WHILE{}".format(jclass.name.upper(), sb.name.upper(), JackCompiler.compile_while.counter)
    label_loop, label_end = label_basic + "_LOOP", label_basic + "_END"
    JackCompiler.compile_while.counter += 1

    self.out.write("label {}\n".format(label_loop))
    self.compile_expression(jclass, sb, whilest.expr)
    self.out.write("not\nif-goto {}\n".format(label_end))
    for statement in whilest.statements:
      self.compile_statement(jclass, sb, statement)
    self.out.write("goto {}\n".format(label_loop))
    self.out.write("label {}\n".format(label_end))

  # st is of type ReturnStatement
  def compile_return(self, jclass, sb, st):
    if st.expr is None:
      self.out.write("push constant 0\n")
    else:
      self.compile_expression(jclass, sb, st.expr)
    self.out.write("return\n")
    
  # ------------------------------------------------------------------

  #
  # expr is an expression, and can be of type int, str (for string
  # literals), ConstantExpression, VariableExpression, UnaryOperation,
  # BinaryOperation, or CallExpression.
  #
  
  def compile_expression(self, jclass, sb, expr):
    if isinstance(expr, int):
      self.out.write("push constant %d\n" % expr)
    if isinstance(expr, str):
      self.compile_literal(expr)
    if isinstance(expr, ConstantExpression):
      self.compile_constant(expr)
    if isinstance(expr, VariableExpression):
      self.compile_variable(jclass, sb, expr)
    if isinstance(expr, CallExpression):
      self.compile_call(jclass, sb, expr)
    if isinstance(expr, BinaryOperation):
      self.compile_binaryop(jclass, sb, expr)
    if isinstance(expr, UnaryOperation):
      self.compile_unaryop(jclass, sb, expr)

  def compile_constant(self, expr):
    if expr.value == "this":
      self.out.write("push pointer 0 // this\n")
    else:
      self.out.write("push constant 0 // %s\n" % expr.value)
      if expr.value == "true":
        self.out.write("not\n")  # true is -1
    
  def compile_literal(self, text):
    self.out.write('push constant %d // "%s"\n' % (len(text), text))
    self.out.write("call String.new 1\n")
    for ch in text:
      self.out.write("push constant %d // '%s'\n" % (ord(ch), ch))
      self.out.write("call String.appendChar 2\n")

  # var is of type VariableExpression
  def compile_variable(self, jclass, sb, var):
    for idx, argument in enumerate(sb.arguments):
      if argument[0] == var.name:
        vm_name = "argument {}".format(idx + (1 if sb.kind == 'method' else 0))
    for idx, local in enumerate(sb.locals):
      if local[0] == var.name:
        vm_name = "local {}".format(idx)
    for idx, static in enumerate(jclass.statics):
      if static[0] == var.name:
        vm_name = "static {}".format(idx)
    for idx, field in enumerate(jclass.fields):
      if field[0] == var.name:
        vm_name = "this {}".format(idx)
    self.out.write("push {}\n".format(vm_name))
    if var.index is not None:
      self.compile_expression(jclass, sb, var.index)
      self.out.write("add\npop pointer 1\npush that 0\n")

  # call is of type CallExpression
  def compile_call(self, jclass, sb, call):
    is_method = False
    if call.container is None: # method_name
      callee = "{}.{}".format(jclass.name, call.name)
      is_method = True
      self.out.write("push pointer 0\n")
    else: # variable.method_name or class_name.function_name
      class_name = None
      for idx, argument in enumerate(sb.arguments):
        if argument[0] == call.container:
          class_name = argument[1]
          self.out.write("push argument {}\n".format(idx + (1 if sb.kind == 'method' else 0)))
      for idx, local in enumerate(sb.locals):
        if local[0] == call.container:
          class_name = local[1]
          self.out.write("push local {}\n".format(idx))
      for idx, static in enumerate(jclass.statics):
        if static[0] == call.container:
          class_name = static[1]
          self.out.write("push static {}\n".format(idx))
      for idx, field in enumerate(jclass.fields):
        if field[0] == call.container:
          class_name = field[1]
          self.out.write("push this {}\n".format(idx))
      if class_name is None: # class_name.function_name
        class_name = call.container
      else:
        is_method = True
      callee = "{}.{}".format(class_name, call.name)
    for argument in call.arguments:
      self.compile_expression(jclass, sb, argument)
    self.out.write("call {} {}\n".format(callee, len(call.arguments) + (1 if is_method else 0)))

  # binop is of type BinaryOperation
  def compile_binaryop(self, jclass, sb, binop):
    self.compile_expression(jclass, sb, binop.left)
    self.compile_expression(jclass, sb, binop.right)
    self.out.write("{}\n".format(binopmap[binop.operator]))

  # unop is of type UnaryOperation
  def compile_unaryop(self, jclass, sb, unop):
    self.compile_expression(jclass, sb, unop.argument)
    self.out.write("not\n" if unop.operator == '~' else "neg\n")
  
# --------------------------------------------------------------------

def main():
  if len(sys.argv) != 2:
    sys.stderr.write("Usage: python3 jackcompiler.py <file.jack>\n")
    sys.stderr.write("    or python3 jackcompiler.py <directory>\n")    
    sys.exit(9)
  path = sys.argv[-1]
  fnames = []
  if path.endswith(".jack"):
    i = path.rfind("/")
    folder = path[:i]
    fnames.append(path)
  else:
    folder = path
    for fname in os.listdir(path):
      if fname.endswith(".jack"):
        fnames.append(path + "/" + fname)
  jclasses = []
  try:
    for fname in fnames:
      jclasses.append(jackparser.parse(fname))
  except jackparser.InputError as e:
    print("Error:", e.msg)
    print("In file '%s', line %d, column %d" %
          (e.token.fname, e.token.lineno, e.token.pos))
    return
  # parsing succeeded, now compile to VM
  compiler = JackCompiler(folder)
  for jclass in jclasses:
    compiler.compile(jclass)

# --------------------------------------------------------------------

if __name__ == "__main__":
  main()

# --------------------------------------------------------------------
