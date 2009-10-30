CLOOP
      SUBROUTINE LOOP
C        HANDLES ALL LOGIC FOR ITERATING TO OBTAIN EXACT CHOKE POINT-
C                  UNDERFLOW, NO CHOKE INITIAL CHOKE, CHOKE ITERATION
C                  SUBCRITICAL, CHOKE ITERATION SUPERCRITICAL,MULTIPLE
C                  CHOKE, CHOKE ITERATION COMPLETE
C
      REAL MFSTOP
      LOGICAL PREVER
      COMMON /SNTCP/G,AJ,PRPC,ICASE,PREVER,MFSTOP,JUMP,LOPIN,ISCASE,
     1KN,GAMF,IP,SCRIT,PTRN,ISECT,KSTG,WTOL,RHOTOL,PRTOL,TRLOOP,LSTG,
     2LBRC,IBRC,ICHOKE,ISORR,CHOKE,PT0PS1(6,8),PTRS2(6,8),TRDIAG,SC,RC,
     3DELPR,PASS,IPC,LOPC,ISS
C
      COMMON /SINPUT/
     1PTPS,PTIN,TTIN,WAIR,FAIR,DELC,DELL,DELA,AACS,BLLD,STG,SECT,EXPN,
     2EXPP,EXPRE,RG,RPM,PAF,SLI,STGCH,ENDJOB,XNAME(20),TITLE(20),
     3PCNH(6),GAM(6,8),DR(6,8),DT(6,8),RWG(6,8),ALPHAS(6,8),ALPHA1(6,8),
     4ETARS(6,8),ETAS(6,8),CFS(6,8),ANDO(6,8),BETA1(6,8),BETA2(6,8),ETAR
     5R(6,8),ETAR(6,8),CFR(6,8),TFR(6,8),ANDOR(6,8),OMEGAS(6,8),AS0(6,8)
     6,ASMP0(6,8),ACMN0(6,8),A1(6,8),A2(6,8),A3(6,8),A4(6,8),A5(6,8),A6(
     76,8),OMEGAR(6,8),BSIA(6,8),BSMPIA(6,8),BCMNIA(6,8),B1(6,8),B2(6,8)
     8,B3(6,8),B4(6,8),B5(6,8),B6(6,8),SESTHI(8),RERTHI(8)
     9,fairx(5,8),wairx(5,8),rg1(8),rg1a(8),rg2(8),rg2a(8)
C
      IJ=8+KSTG
C     INCREASE BLADE ROW COUNTER
c     WRITE(16,2001)IBRC,LBRC,ISORR,KN,LSTG,IPC,ISS,ICHOKE,JUMP,LBRCS,
c    1ISORRS,LSTGS,SPTPS,PT0PS1(IP,JL),DELPR,DELL,SCRIT,LOPC
      if (delpr.lt.prtol/20.) go to 100
      IBRC=IBRC+1
C     TEST NEGATIVE SECTOR PRESSURE RATIO
      IF (PTRN)18,1,1
C     TEST CHOKE ITERATION ON BLADE ROW
1     IF (ICHOKE-IBRC)3,2,3
C     TEST INCREMENT TOLERANCE
2     IF (PRTOL-DELPR)3,3,4
C     TEST STATION FLOW CRITICAL
3     IF (SCRIT)5,5,6
C     CHOKE ITERATION COMPLETE
4     ICHOKE=0
      IPC=IBRC
      ISS=IBRC
      ISORR=2+(IBRC/2)*2-IBRC
      JL=(ISORR-1)*8+KN
      IF (JL-IJ)22,23,23
22    DELPR=DELL
24    LOPC=0
      CHOKE=1.
      LSTG=KN
      LBRC=IBRC-1
      GO TO 18
23    DELPR=DELA
      GO TO 24
5     IF (ICHOKE-IBRC)18,7,18
C     TEST CHOKE ITERATION LOOP
6     IF(ISS-IBRC)8,18,18
C     CHOKE ITERATION
C     ISORR = 1 FOR STATOR
C           = 2 FOR ROTOR
7     DELPR=DELPR/2.
      JL=(ISORR-1)*8+LSTG
      PT0PS1(IP,JL)=PT0PS1(IP,JL)+DELPR
      GO TO 16
C     CHOKE HAS OCURRED
8     IF(ICHOKE)80,80,13
80    J=(IBRC-2*(KN-1)-1)*8+KN
c error in index calculation above
	if (j.gt.8) then
	 WRITE(16,801)IBRC,PTrs2(IP,J-8)
	 else
      WRITE(16,801)IBRC,PT0PS1(IP,J)
	endif
801   FORMAT(16X,10HBLADE ROW ,I3,8H CHOKED ,4X,5HPTPS=,F10.5)
C     TEST SINGLE CALCULATION POINT
9     IF (DELC)18,18,10
C     TEST PREVIOUS CHOKE
10    IF (IPC)11,11,12
C     SAVE COMBINATIONS PRIOR FIRST CHOKE
11    LBRCS=LBRC
      ISORRS=ISORR
      JL=(ISORR-1)*8+LSTG
      SPTPS=PT0PS1(IP,JL)-DELPR
      LSTGS=LSTG
      SDELPR=DELPR
      GO TO 13
12    continue
      JL=LSTGS+(ISORRS-1)*8
      DELNU = (PT0PS1(IP,JL)-SPTPS)/4.
      IF (DELNU.LE.0.0001) DELNU = SDELPR/4.
      DELPR = DELNU
      SDELPR = DELNU
      WRITE(16,1201)IPC,IBRC,DELPR
1201  FORMAT(6X,11HBLADE ROWS ,I5,5H AND ,I5,' CHOKED - INCREMENT NOW ',
     1F10.5)
      LBRC=LBRCS
      LSTG=LSTGS
      ISORR=ISORRS
      PT0PS1(IP,JL) = SPTPS + SDELPR
      LOPC=10
      ICHOKE=0
      IPC=0
      ISS=LBRC+1
      CHOKE=0.0
      GO TO 17
C     TEST PREVIOUS COMPLETE CALCULATION
13    IF (PASS)15,15,14
14    ICHOKE=IBRC
      DELPR=.5*DELPR
15    JL=(ISORR-1)*8+LSTG
      PT0PS1(IP,JL)=PT0PS1(IP,JL)-DELPR
C     SET INDEX REGISTERS
16    CONTINUE
      LOPC=LOPC+1
C SET JUMP FOR CHOKE ITERATION
17    JUMP=1
      GO TO 19
C     JUMP SET FOR NO CHOKE OR CHOKE COMPLETE
18    JUMP=0
C     TEST LOOP-TRACE
19    IF (TRLOOP)21,21,20
20    WRITE(16,2001)IBRC,LBRC,ISORR,KN,LSTG,IPC,ISS,ICHOKE,JUMP,LBRCS,
     1ISORRS,LSTGS,SPTPS,PT0PS1(IP,JL),DELPR,DELL,SCRIT,LOPC
2001  FORMAT(3X,12I5/3X,4F10.5,F10.3,I10)
21    RETURN
  100 write (16,2005)
 2005 format(/'0 **** CHOKE CONVERGENCE PROBLEM - SET INPUT VARIABLE ICF
     &=1 AND RERUN ****')
      STOP
      END
