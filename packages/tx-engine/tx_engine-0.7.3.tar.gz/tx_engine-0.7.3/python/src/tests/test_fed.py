#!/usr/bin/python3
import unittest

from tx_engine import Script, Context, encode_num, Stack

from tx_engine.engine.op_codes import (
    OP_1,
    OP_DEPTH, OP_1SUB, OP_PICK, OP_EQUALVERIFY, OP_ROT, OP_TOALTSTACK,
    OP_ROLL, OP_TUCK, OP_OVER, OP_ADD, OP_MOD, OP_FROMALTSTACK, OP_SWAP,
    OP_MUL, OP_2,
    OP_EQUAL,
)

from test_parse import values_to_bytes


class FedTest(unittest.TestCase):
    # maxDiff = None
    def test_federico1(self):
        input_script = Script.parse_string("19 1 0 0 1")
        self.assertEqual(input_script.cmds, values_to_bytes([1, 19, OP_1, 0, 0, OP_1]))

    def test_federico2(self):
        script1 = Script.parse_string('19 1 0 0 1 OP_DEPTH OP_1SUB OP_PICK 0x13 OP_EQUALVERIFY OP_ROT OP_ADD OP_TOALTSTACK OP_ADD OP_DEPTH OP_1SUB OP_ROLL OP_TUCK OP_MOD OP_OVER OP_ADD OP_OVER OP_MOD OP_FROMALTSTACK OP_ROT OP_TUCK OP_MOD OP_OVER OP_ADD OP_SWAP OP_MOD 1 OP_EQUALVERIFY 1 OP_EQUAL')
        self.assertEqual(script1.cmds, values_to_bytes([1, 19, OP_1, 0, 0, OP_1, OP_DEPTH, OP_1SUB, OP_PICK, 1, 19, OP_EQUALVERIFY, OP_ROT, OP_ADD, OP_TOALTSTACK, OP_ADD, OP_DEPTH, OP_1SUB, OP_ROLL, OP_TUCK, OP_MOD, OP_OVER, OP_ADD, OP_OVER, OP_MOD, OP_FROMALTSTACK, OP_ROT, OP_TUCK, OP_MOD, OP_OVER, OP_ADD, OP_SWAP, OP_MOD, OP_1, OP_EQUALVERIFY, OP_1, OP_EQUAL]))
        context = Context(script=script1)
        context.evaluate_core()
        # Should leave [1] on the stack
        self.assertEqual(context.get_stack(), Stack([[1]]))

    def test_federico3(self):
        script1 = Script.parse_string('OP_2 OP_1 OP_SUB')
        context = Context(script=script1)
        context.evaluate()
        self.assertEqual(context.get_stack(), Stack([[1]]))

    def test_federico4(self):
        x = encode_num(53758635199196621832532654341949827999954483761840054390272371671254106983912)
        self.assertEqual(x, b'\xe8ME\xca\xabI\x1a7:$#+\x91\xe2\xab`%\xce`3Y\xc0\x064\xde\x0f\x8fU+O\xdav')

    def test_federico5(self):
        script1 = Script.parse_string('OP_2 OP_1 OP_MUL')
        self.assertEqual(script1.cmds, values_to_bytes([OP_2, OP_1, OP_MUL]))
        context = Context(script=script1)
        context.evaluate()
        self.assertEqual(context.get_stack(), Stack([[2]]))

        script1 = Script.parse_string('OP_MUL')
        self.assertEqual(script1.cmds, values_to_bytes([OP_MUL]))

    def test_federico6(self):
        q = encode_num(41898490967918953402344214791240637128170709919953949071783502921025352812571106773058893763790338921418070971888253786114353726529584385201591605722013126468931404347949840543007986327743462853720628051692141265303114721689601)
        script1 = Script.parse_string("0x" + q.hex())

        script2 = Script()
        script2.append_pushdata(q)
        self.assertEqual(script1, script2)

    def test_federico7(self):
        script1 = Script.parse_string('1000')
        script2 = Script.parse_string(script1.to_string())
        self.assertEqual(script1, script2)

    def test_federico8(self):
        random = 557 * 8
        script1 = Script()
        script1.append_pushdata(random.to_bytes(557, 'big'))
        context = Context(script=script1)
        context.evaluate()
        test_stack: Stack = Stack()
        test_stack.push_bytes_integer([997082905641431491405618212310581424398970582693777201057910160273107676142762986033552521885002886512679322285950807583723151399865653540206311599969131480522591113580368679142386215063365626477686804777423891146474440661477197646978357827947106506012143586661042378705229988584443402589850656136383304667560356971070271571401609380425486414046680173847621616669803698336474564482164685921199981121725357169234695512899349306660307773194255798717381470675052513899639735941264294985837331216053312582013805728660983334532212689718199656864764791843042669433609159344560312198927395970196018235746115495595144830656307000990085825787949248031793190718625660223069226379257102506037424430036760952158340779889870572933112659610492841653854561723623789285692008207231789356520165176197713626602667068831126096587431549352800404296204923059336487520013061294428163874562159217191450195849333382804096117692262170938573817853022445950766849398169558014709010119476858678603343219290621940748923679384067778858250625703825822117104464506908071731197550261212714623568812501065645317742591220318558333063347051562809020567992710830048749279613579078870288417477704238464033357036491865389500921661587707155913717686845285474235674957552200028304867198968704462190471630727428015401298096702407188499334952031658427624138455857703602775127192764416])
        self.assertEqual(context.stack, test_stack)
        script2 = Script.parse_string(script1.to_string())
        context = Context(script=script2)
        context.evaluate()
        self.assertEqual(context.get_stack(), test_stack)

    def test_federico9(self):
        script1 = Script.parse_string('0x0100 OP_BIN2NUM OP_1 OP_EQUAL')
        context = Context(script=script1)
        self.assertTrue(context.evaluate())

    def test_federico10(self):
        test = Script.parse_string('OP_1 OP_2 OP_NUM2BIN 0x0100 OP_EQUAL')
        context = Context(script=test)
        self.assertTrue(context.evaluate())


if __name__ == '__main__':
    unittest.main()
