from sly import Parser

import pb_lexer

class BasicParser(Parser):
    tokens = pb_lexer.BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }
    @_('')
    def statement(self, p):
        pass

    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return ('garang_gawe', ('persiyapan_garang_gawe', p.var_assign, p.expr), p.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('pratelan_nek', p.condition, ('cabang', p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('definisi_fungsi', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('undangane_fungsi', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('kahanan_dobel_podokaro', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('nemtokake_variabel', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('nemtokake_variabel', p.NAME, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('lan', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sudo', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('ping', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('poro', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('variabel', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('nomer', p.NUMBER)
        
    @_('PRINT expr')
    def expr(self, p):
        return ('cethak', p.expr)

    @_('PRINT STRING')
    def statement(self, p):
        return ('cethak', p.STRING)

if __name__ == '__main__':
    lexer = pb_lexer.BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('PhiBee > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
            