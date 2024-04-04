from enum import Enum

class Status(Enum):
    S100 = 100
    S110 = 110
    S120 = 120
    S125 = 125
    S150 = 150
    S200 = 200
    S202 = 202
    S211 = 211
    S212 = 212
    S213 = 213
    S214 = 214
    S215 = 215
    S220 = 220
    S221 = 221
    S225 = 225
    S226 = 226
    S227 = 227
    S228 = 228
    S229 = 229
    S230 = 230
    S232 = 232
    S234 = 234
    S235 = 235
    S250 = 250
    S257 = 257
    S300 = 300
    S331 = 331
    S332 = 332
    S334 = 334
    S335 = 335
    S336 = 336
    S350 = 350
    S400 = 400
    S421 = 421
    S425 = 425
    S426 = 426
    S430 = 430
    S431 = 431
    S434 = 434
    S450 = 450
    S451 = 451
    S452 = 452
    S500 = 500
    S501 = 501
    S502 = 502
    S503 = 503
    S504 = 504
    S530 = 530
    S532 = 532
    S533 = 533
    S534 = 534
    S535 = 535
    S536 = 536
    S537 = 537
    S550 = 550
    S551 = 551
    S552 = 552
    S553 = 553
    S600 = 600
    S631 = 631
    S632 = 632
    S633 = 633
    S10000 = 10000
    S10054 = 10054
    S10060 = 10060
    S10061 = 10061
    S10065 = 10065
    S10066 = 10066
    S10068 = 10068

    @staticmethod
    def is_positive_preliminary(status):
        return 100 <= status.value < 200

    @staticmethod
    def is_positive_completion(status):
        return 200 <= status.value < 300

    @staticmethod
    def is_positive_intermediate(status):
        return 300 <= status.value < 400

    @staticmethod
    def is_negative4xx(status):
        return 400 <= status.value < 500

    @staticmethod
    def is_negative5xx(status):
        return 500 <= status.value < 600
