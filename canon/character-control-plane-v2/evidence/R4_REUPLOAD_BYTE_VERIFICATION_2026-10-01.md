# R4 Re-upload Byte Verification Receipt — 2026-10-01

**Branch:** memo-os/v5-6-publication-integrity
**Checkpoint:** exact-byte materialization + SHA-256 verification after Commissioner re-upload
**Result:** PARTIAL PASS / 2 EXACT / 10 HASH-MISMATCH QUARANTINE
**R4:** HOLD
**Page 1 generation:** BLOCKED

## Materialization result
All 12 newly supplied image attachments now have an authorized raw-byte materialization path and were successfully copied into the execution container. This resolves the previous blanket raw-byte transport failure for these uploaded attachments.

## Exact canonical hash comparison
The active Commissioner Reference Register remains the byte-identity authority. No hash was silently replaced.

### Exact matches — PASS
- CHAR-PHILLIP-PITTS / Three Dreaded Snake
  - uploaded: IMG_2178(2).jpeg
  - observed SHA-256: 31b9d7be295ba662b1332897ef7c33e2f64e92aeefb2d6abe625c08bac914c0c
  - canonical SHA-256: 31b9d7be295ba662b1332897ef7c33e2f64e92aeefb2d6abe625c08bac914c0c
  - result: EXACT PASS
- CHAR-AUSTIN-BYARS / His Majesty's Blood
  - uploaded: IMG_2179(1).jpeg
  - observed SHA-256: eedfaaf0b2e2dd78a7a32e11aef333cab41278c206b65ec78c4aa4f1fd2c4f76
  - canonical SHA-256: eedfaaf0b2e2dd78a7a32e11aef333cab41278c206b65ec78c4aa4f1fd2c4f76
  - result: EXACT PASS

### Re-uploaded bytes — QUARANTINE pending identity ruling
The remaining ten uploads materialized successfully but their SHA-256 values do not equal the registered canonical byte hashes. They may be screenshots/PNG exports or other encodings of visually related approved art; byte identity is therefore not proven and the existing R4 contract requires fail-closed handling.

Observed hashes:
- Screenshot 2026-08-28 at 15.33.58(4).png — 291cdcdb8cb7504f66b556208c774d88dec0979e6fe25c68783b272541c63f70
- Screenshot 2026-08-28 at 15.34.43(4).png — 4752363b8e55dabd530caf74bdeb2da4feaee3870377d96c3c7f5eac7027f32c
- Screenshot 2026-08-28 at 15.34.06(4).png — b5b0b10e06cf0598bdc9e3501c170d14529bdb4dee31f8ee3453a40048a6099c
- Screenshot 2026-08-28 at 15.34.24(4).png — 33e70a9208b47692d9d883707236a2b3a670629e0cb3b3f84c61eacff20fea37
- Screenshot 2026-08-28 at 15.32.41(4).png — 5ff6fc4fc0b2f37d76bbab8651400478e37a709418867b0fd111c993762f9eda
- ChatGPT Image Sep 24, 2026 at 03_53_33 PM.png — cc35af31973f2a35fe0231a269923234185f9908a67545d2b2e1190d052ad9a1
- 0D748D18-AF18-481E-AD99-428D5DC95F9A(3).png — 17ee4bcfcd774ac649ca96df01522f16d7c4fd626f9bdd047faefa3a4d381319
- Screenshot 2026-08-28 at 15.33.47(4).png — 462e5d6517b5653458c8d32c20692e94d037b134de7aac18325c1af41647eefc
- Screenshot 2026-08-28 at 15.34.34(4).png — 535d984397cd7aeeda0b83b652d35b4975fd4c0f6c52230174201720ec41a655
- IMG_7866.PNG — 8f64dfcfc1ceae4f737320e33dbfe296a0aae35ff4552af35f791e6b0615703a

## Important finding
The current upload has materially improved R4:
- raw-byte materialization: 12/12 PASS;
- exact registered byte identity: 2/12 PASS;
- mismatched uploads: 10/12 QUARANTINED;
- silent canonical-hash mutation: 0;
- prose reconstruction: 0;
- renderer mount receipt: not yet authorized for the 10 mismatches;
- ensemble Page 1 generation remains blocked because it requires all 12 current references.

## Next checkpoint
Character Authority + Librarian must map the ten materialized uploads to owner identities using the visible approved-reference evidence and determine one of two legal outcomes per asset:
A. locate/re-upload the exact original binary matching the existing canonical SHA-256; or
B. Commissioner explicitly promotes the newly uploaded binary as the replacement canonical PRIMARY, after which its new hash can be registered with provenance/supersession.

Until one of those paths is completed, do not mutate the Commissioner Reference Register and do not generate the 12-character ensemble.
