import pygame, sys, numpy as np, time
from copy import deepcopy

pygame.init()

WID, HEI = 800, 800
RWS, CLS = 8, 8
SQ_SZ = WID // CLS

DRK_BRN = (139, 69, 19)
LGT_BRN = (222, 184, 135)
WHT = (245, 245, 220)
RD = (220, 20, 60)
BLK = (0, 0, 0)
BLU = (0, 191, 255)
GRY = (128, 128, 128)
CRWN = (255, 215, 0)
SHDW = (50, 50, 50, 100)
GRN = (0, 128, 0)

SCRN = pygame.display.set_mode((WID, HEI))
pygame.display.set_caption('Checkers Game')

FNT = pygame.font.SysFont('Arial', 30, bold=True)
SM_FNT = pygame.font.SysFont('Arial', 24)

class Pce:
    PAD = 15
    OUTLN = 2
    def __init__(self, rw, cl, clr):
        self.rw = rw
        self.cl = cl
        self.clr = clr
        self.kng = False
        self.x_pos = 0
        self.y_pos = 0
        def calc():
            self.x_pos = SQ_SZ * self.cl + SQ_SZ // 2
            self.y_pos = SQ_SZ * self.rw + SQ_SZ // 2
        calc()

    def mk_kng(self):
        self.kng = True

    def drw(self, scn):
        def draw_circs():
            rad = SQ_SZ // 2 - self.PAD
            pygame.draw.circle(scn, SHDW, (self.x_pos + 5, self.y_pos + 5), rad)
            pygame.draw.circle(scn, GRY, (self.x_pos, self.y_pos), rad + self.OUTLN)
            pygame.draw.circle(scn, self.clr, (self.x_pos, self.y_pos), rad)
            if self.kng:
                pygame.draw.circle(scn, CRWN, (self.x_pos, self.y_pos), rad // 2)
        draw_circs()

    def mv(self, rw, cl):
        self.rw = rw
        self.cl = cl
        def recalc():
            self.x_pos = SQ_SZ * self.cl + SQ_SZ // 2
            self.y_pos = SQ_SZ * self.rw + SQ_SZ // 2
        recalc()

    def __repr__(self):
        return str(self.clr)

class Brd:
    def __init__(self):
        self.brd = []
        self.rd_cnt = self.wht_cnt = 12
        self.rd_kngs = self.wht_kngs = 0
        def setup():
            for r in range(RWS):
                self.brd.append([])
                for c in range(CLS):
                    if c % 2 == ((r + 1) % 2):
                        if r < 3:
                            self.brd[r].append(Pce(r, c, WHT))
                        elif r > 4:
                            self.brd[r].append(Pce(r, c, RD))
                        else:
                            self.brd[r].append(0)
                    else:
                        self.brd[r].append(0)
        setup()

    def drw_sqs(self, scn):
        scn.fill(DRK_BRN)
        for r in range(RWS):
            for c in range(r % 2, RWS, 2):
                pygame.draw.rect(scn, LGT_BRN, (r * SQ_SZ, c * SQ_SZ, SQ_SZ, SQ_SZ))

    def eval_brd(self):
        return self.wht_cnt - self.rd_cnt + (self.wht_kngs * 0.5 - self.rd_kngs * 0.5)

    def gt_pcs(self, clr):
        pcs = []
        def collect():
            for rw in self.brd:
                for pc in rw:
                    if pc != 0 and pc.clr == clr:
                        pcs.append(pc)
        collect()
        return pcs

    def mv_pc(self, pc, rw, cl):
        self.brd[pc.rw][pc.cl], self.brd[rw][cl] = self.brd[rw][cl], self.brd[pc.rw][pc.cl]
        pc.mv(rw, cl)
        def chk_kng():
            if rw == RWS - 1 or rw == 0:
                pc.mk_kng()
                if pc.clr == WHT:
                    self.wht_kngs += 1
                else:
                    self.rd_kngs += 1
        chk_kng()

    def gt_pc(self, rw, cl):
        return self.brd[rw][cl]

    def drw(self, scn):
        def render():
            self.drw_sqs(scn)
            for r in range(RWS):
                for c in range(CLS):
                    pc = self.brd[r][c]
                    if pc != 0:
                        pc.drw(scn)
        render()

    def rmv(self, pcs):
        for pc in pcs:
            self.brd[pc.rw][pc.cl] = 0
            if pc != 0:
                if pc.clr == RD:
                    self.rd_cnt -= 1
                else:
                    self.wht_cnt -= 1

    def wnr(self):
        if self.rd_cnt <= 0:
            return WHT
        elif self.wht_cnt <= 0:
            return RD
        return None

    def gt_vld_mvs(self, pc):
        mvs = {}
        lft = pc.cl - 1
        rgt = pc.cl + 1
        rw = pc.rw
        def chk_dirs():
            if pc.clr == RD or pc.kng:
                mvs.update(self._trv_lft(rw - 1, max(rw - 3, -1), -1, pc.clr, lft))
                mvs.update(self._trv_rgt(rw - 1, max(rw - 3, -1), -1, pc.clr, rgt))
            if pc.clr == WHT or pc.kng:
                mvs.update(self._trv_lft(rw + 1, min(rw + 3, RWS), 1, pc.clr, lft))
                mvs.update(self._trv_rgt(rw + 1, min(rw + 3, RWS), 1, pc.clr, rgt))
        chk_dirs()
        return mvs

    def _trv_lft(self, st, sp, stp, clr, lft, skp=[]):
        mvs = {}
        lst = []
        for r in range(st, sp, stp):
            if lft < 0:
                break
            curr = self.brd[r][lft]
            if curr == 0:
                if skp and not lst:
                    break
                elif skp:
                    mvs[(r, lft)] = lst + skp
                else:
                    mvs[(r, lft)] = lst
                if lst:
                    def cont():
                        if stp == -1:
                            rw = max(r - 3, -1)
                        else:
                            rw = min(r + 3, RWS)
                        mvs.update(self._trv_lft(r + stp, rw, stp, clr, lft - 1, skp=lst))
                        mvs.update(self._trv_rgt(r + stp, rw, stp, clr, lft + 1, skp=lst))
                    cont()
                break
            elif curr.clr == clr:
                break
            else:
                lst = [curr]
            lft -= 1
        return mvs

    def _trv_rgt(self, st, sp, stp, clr, rgt, skp=[]):
        mvs = {}
        lst = []
        for r in range(st, sp, stp):
            if rgt >= CLS:
                break
            curr = self.brd[r][rgt]
            if curr == 0:
                if skp and not lst:
                    break
                elif skp:
                    mvs[(r, rgt)] = lst + skp
                else:
                    mvs[(r, rgt)] = lst
                if lst:
                    def cont():
                        if stp == -1:
                            rw = max(r - 3, -1)
                        else:
                            rw = min(r + 3, RWS)
                        mvs.update(self._trv_lft(r + stp, rw, stp, clr, rgt - 1, skp=lst))
                        mvs.update(self._trv_rgt(r + stp, rw, stp, clr, rgt + 1, skp=lst))
                    cont()
                break
            elif curr.clr == clr:
                break
            else:
                lst = [curr]
            rgt += 1
        return mvs

class Gm:
    def __init__(self, scn):
        self.rst_btn = pygame.Rect(WID - 120, HEI - 50, 100, 40)
        def init_gm():
            self.slctd = None
            self.brd = Brd()
            self.trn = RD
            self.vld_mvs = {}
            self.thnk = False
            self.thnk_dts = 0
            self.thnk_tm = 0
        init_gm()
        self.scn = scn

    def upd(self):
        def do_upd():
            self.drw_bck()
            self.brd.drw(self.scn)
            self.drw_vld_mvs(self.vld_mvs)
            self.drw_ui()
            pygame.display.update()
        do_upd()

    def drw_bck(self):
        for y in range(HEI):
            clr = (
                int(50 + (y / HEI) * 50),
                int(50 + (y / HEI) * 100),
                int(100 + (y / HEI) * 50)
            )
            pygame.draw.line(self.scn, clr, (0, y), (WID, y))

    def drw_ui(self):
        def ui_rndr():
            trn_txt = f"{'Red' if self.trn == RD else 'White'}'s Turn"
            trn_srf = FNT.render(trn_txt, True, WHT)
            self.scn.blit(trn_srf, (20, 10))
            rd_cnt = SM_FNT.render(f"Red count: {self.brd.rd_cnt}", True, RD)
            wht_cnt = SM_FNT.render(f"White count: {self.brd.wht_cnt}", True, WHT)
            self.scn.blit(rd_cnt, (20, 50))
            self.scn.blit(wht_cnt, (20, 70))
            if self.thnk:
                dts = '.' * (int(self.thnk_dts) % 4)
                thnk_txt = FNT.render(f"White AI is thinking{dts}", True, WHT)
                self.scn.blit(thnk_txt, (20, 100))
            wnr = self.brd.wnr()
            if wnr:
                wnr_clr = 'Red' if wnr == RD else 'White'
                wn_txt = FNT.render(f"{wnr_clr} Wins!", True, GRN)
                self.scn.blit(wn_txt, (WID // 2 - wn_txt.get_width() // 2, HEI // 2))
            pygame.draw.rect(self.scn, GRN, self.rst_btn)
            rst_txt = SM_FNT.render('Reset', True, WHT)
            self.scn.blit(rst_txt, (WID - 110, HEI - 45))
        ui_rndr()

    def rst(self):
        def do_rst():
            self.slctd = None
            self.brd = Brd()
            self.trn = RD
            self.vld_mvs = {}
            self.thnk = False
        do_rst()

    def slct(self, rw, cl):
        def try_mv():
            if self.slctd:
                rslt = self._mv(rw, cl)
                if not rslt:
                    self.slctd = None
                    self.slct(rw, cl)
        try_mv()
        pc = self.brd.gt_pc(rw, cl)
        if pc != 0 and pc.clr == self.trn:
            self.slctd = pc
            self.vld_mvs = self.brd.gt_vld_mvs(pc)
            return True
        return False

    def _mv(self, rw, cl):
        pc = self.brd.gt_pc(rw, cl)
        if self.slctd and pc == 0 and (rw, cl) in self.vld_mvs:
            self.brd.mv_pc(self.slctd, rw, cl)
            skp = self.vld_mvs[(rw, cl)]
            if skp:
                self.brd.rmv(skp)
            self.chg_trn()
            return True
        return False

    def drw_vld_mvs(self, mvs):
        for mv in mvs:
            r, c = mv
            pygame.draw.circle(self.scn, BLU, (c * SQ_SZ + SQ_SZ // 2, r * SQ_SZ + SQ_SZ // 2), 15)

    def chg_trn(self):
        self.vld_mvs = {}
        self.slctd = None
        if self.trn == RD:
            self.trn = WHT
        else:
            self.trn = RD

    def gt_brd(self):
        return self.brd

    def ai_mv(self, brd):
        self.brd = brd
        self.chg_trn()

def mmx(pos, dpth, mx_plr, gm):
    def eval_pos():
        if dpth == 0 or pos.wnr() is not None:
            return pos.eval_brd(), pos
        if mx_plr:
            mx_ev = float('-inf')
            bst_mv = None
            for mv in gt_all_mvs(pos, WHT, gm):
                ev = mmx(mv, dpth - 1, False, gm)[0]
                mx_ev = max(mx_ev, ev)
                if mx_ev == ev:
                    bst_mv = mv
            return mx_ev, bst_mv
        else:
            mn_ev = float('inf')
            bst_mv = None
            for mv in gt_all_mvs(pos, RD, gm):
                ev = mmx(mv, dpth - 1, True, gm)[0]
                mn_ev = min(mn_ev, ev)
                if mn_ev == ev:
                    bst_mv = mv
            return mn_ev, bst_mv
    return eval_pos()

def sim_mv(pc, mv, brd, gm, skp):
    brd.mv_pc(pc, mv[0], mv[1])
    if skp:
        brd.rmv(skp)
    return brd

def gt_all_mvs(brd, clr, gm):
    mvs = []
    def collect_mvs():
        for pc in brd.gt_pcs(clr):
            vld_mvs = brd.gt_vld_mvs(pc)
            for mv, skp in vld_mvs.items():
                tmp_brd = deepcopy(brd)
                tmp_pc = tmp_brd.gt_pc(pc.rw, pc.cl)
                new_brd = sim_mv(tmp_pc, mv, tmp_brd, gm, skp)
                mvs.append(new_brd)
    collect_mvs()
    return mvs

def mn():
    rn = True
    clk = pygame.time.Clock()
    gm = Gm(SCRN)
    lst_upd = time.time()
    while rn:
        clk.tick(60)
        if gm.thnk:
            if time.time() - lst_upd > 0.3:
                gm.thnk_dts += 1
                lst_upd = time.time()
        def ai_thnk():
            if gm.trn == WHT and not gm.brd.wnr():
                gm.thnk = True
                gm.upd()
                val, new_brd = mmx(gm.gt_brd(), 5, True, gm)
                gm.ai_mv(new_brd)
                gm.thnk = False
        ai_thnk()
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                rn = False
            if evt.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rw, cl = pos[1] // SQ_SZ, pos[0] // SQ_SZ
                if gm.rst_btn.collidepoint(pos):
                    gm.rst()
                if gm.trn == RD and not gm.brd.wnr():
                    gm.slct(rw, cl)
        gm.upd()
    pygame.quit()

if __name__ == "__main__":
    mn()