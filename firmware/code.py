import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.split import Split
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap, HoldTapRepeat
import scanner
import os

keyboard = KMKKeyboard()

low_threshold=2.0
high_threshold=2.1

S1 = 0
S2 = 1
S3 = 2
S4 = 3
S5 = 4
S6 = 5
S7 = 6
S8 = 7

row_pins = (board.D5, board.D4, board.D3, board.D6)
adc_port = board.A0
discharge_port = board.D10
mux_sels = (board.D9, board.D8, board.D7)
col_channels=[S8, S6, S4, S1, S2, S3]
data_pin = board.D2
tap_time = 125

holdtap = HoldTap()
holdtap.tap_time = tap_time
holdtap.prefer_hold = False
keyboard.modules.append(holdtap)

layer = Layers()
layer.tap_time = tap_time
layer.prefer_hold = True
keyboard.modules.append(layer)

split = Split(
    use_pio=True,
    data_pin=data_pin,
    uart_interval=5,
)
keyboard.modules.append(split)

keyboard.coord_mapping = [
    0, 1, 2, 3, 4, 5,       24, 25, 26, 27, 28, 29,
    6, 7, 8, 9, 10, 11,     30, 31, 32, 33, 34, 35,
    12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41,
    18, 19, 20, 21, 22, 23, 42, 43, 44, 45, 46, 47
]

_lower = 1
_raise = 2
_adjust = 3

Lower = KC.MO(_lower)
Raise = KC.MO(_raise)
Adjust = KC.MO(_adjust)

EscGUI = KC.HT(KC.ESC, KC.RGUI, repeat=HoldTapRepeat.HOLD)
LowMins = KC.LT(_lower, KC.MINS, repeat=HoldTapRepeat.HOLD)
AdjEnt = KC.LT(_adjust, KC.ENT, repeat=HoldTapRepeat.HOLD)
AdjMins = KC.LT(_adjust, KC.MINS, repeat=HoldTapRepeat.HOLD)
Adjust = KC.MO(_adjust)
RaiEnt = KC.LT(_raise, KC.ENT, prefer_hold=True, repeat=HoldTapRepeat.HOLD)
Sands = KC.HT(KC.SPC, KC.RSFT, repeat=HoldTapRepeat.HOLD)
xxxxx = KC.NO

keyboard.keymap = [
    # Test
    # [
    #     KC.GRV , KC.N1  , KC.N2  , KC.N3  , KC.N4  ,  KC.N5  ,      KC.N6  , KC.N7  , KC.N8  , KC.N9  , KC.N0  , KC.Z   ,
    #     KC.A   , KC.B   , KC.C   , KC.D   , KC.E   ,  KC.F   ,      KC.G   , KC.H   , KC.I   , KC.J   , KC.K   , KC.L   ,
    #     KC.M   , KC.N   , KC.O   , KC.P   , KC.Q   ,  KC.R   ,      KC.S   , KC.T   , KC.U   , KC.V   , KC.W   , KC.X   ,
    #     KC.Y   , KC.Z   , KC.COMM, KC.DOT , KC.SPC ,  KC.PIPE,      KC.LPRN, KC.RPRN, KC.SLSH, KC.LCBR, KC.SCLN, KC.QUOT,
    # ],
    # QWERTY
    [
        KC.TAB , KC.Q   , KC.W   , KC.E   , KC.R   ,  KC.T   ,      KC.Y   , KC.U   , KC.I   , KC.O   , KC.P   , KC.BSPC,
        KC.ESC , KC.A   , KC.S   , KC.D   , KC.F   ,  KC.G   ,      KC.H   , KC.J   , KC.K   , KC.L   , KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z   , KC.X   , KC.C   , KC.V   ,  KC.B   ,      KC.N   , KC.M   , KC.COMM, KC.DOT , KC.SLSH, KC.ENT ,
        Adjust , KC.LCTL, KC.LALT, KC.LGUI, Lower  ,  KC.SPC ,      KC.SPC , Raise  , KC.LEFT, KC.DOWN, KC.UP  , KC.RGHT
    ],
    # Lower
    [
        KC.TILD, KC.EXLM, KC.AT  , KC.HASH, KC.DLR ,  KC.PERC,      KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL ,
        KC.DEL , KC.F1  , KC.F2  , KC.F3  , KC.F4  ,  KC.F5  ,      KC.F6  , KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE,
        xxxxx  , KC.F7  , KC.F8  , KC.F9  , KC.F10 ,  KC.F11 ,      KC.F12 , KC.TILD, KC.PIPE, xxxxx  , xxxxx  , xxxxx  ,
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx
    ],
    # Raise
    [
        KC.GRV , KC.N1  , KC.N2  , KC.N3  , KC.N4  ,  KC.N5  ,      KC.N6  , KC.N7  , KC.N8  , KC.N9  , KC.N0  , KC.DEL ,
        KC.DEL , KC.F1  , KC.F2  , KC.F3  , KC.F4  ,  KC.F5  ,      KC.F6  , KC.MINS, KC.EQL , KC.LBRC, KC.RBRC, KC.BSLS,
        xxxxx  , KC.F7  , KC.F8  , KC.F9  , KC.F10 ,  KC.F11 ,      KC.F12 , KC.HASH, KC.SLSH, xxxxx  , xxxxx  , xxxxx  ,
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx
    ],
    # Adjust
    [
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  ,
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  ,
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  ,
        xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx   ,      xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx  , xxxxx
    ],
]

keyboard.matrix = scanner.ECMatrixScanner(
    col_channels=col_channels,
    rows=row_pins,
    mux_sels=mux_sels,
    adc_port=adc_port,
    discharge_port=discharge_port,
    low_threshold=low_threshold,
    high_threshold=high_threshold,
    debug=os.getenv('DEBUG', 0) == 1,
)

keyboard.debug_enabled = False
if __name__ == '__main__':
    keyboard.go()
