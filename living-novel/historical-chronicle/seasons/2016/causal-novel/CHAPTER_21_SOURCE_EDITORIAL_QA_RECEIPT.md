# Chapter XXI — Source and Editorial QA Receipt (NONCANON)

**Draft:** THE_BOOK_THAT_WALKED_OUT_CHAPTER_21_NONCANON.md
**Assembled reader:** READING_COPY_CAUSAL_CHAPTERS_01_21_NONCANON.md
**Existing PR:** #243; branch novel/historical-epic-2015-2026
**Date:** 2026-10-30
**Status:** Author-side editorial and mechanical verification only. Independent Authors Council, 2016 Character Canon, Atlas, Librarian and Umpire acceptance NOT OBSERVED.

## Work actually completed

- Wrote a five-movement Chapter XXI: **6,218 whitespace-separated words including editorial handoff**, Git blob 6badbdcaa4bad10313cb5de6ccbca8711c24a4e4.
- Advanced the continuous source-component reader to **21 chapters / 109,944 whitespace-separated words**, Git blob 322138c36de8bf80cf01b41b7870203bc70fd205; preceding 20-chapter reader retained at Git blob b150c37f0d8adda70359bb8a53d05079b9212631.
- Added **17 new Python regression methods** in test_2016_causal_chapter_twenty_one_reader.py (Git blob a55773f109de50b7119caccf75f9d03ec6d3369a).
- **Observed Mac test execution at checkout faa1137d16396b280d7d7430faf1c31bb5bb34cf:** command python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -q; **228 tests, 0 failures**. An initial run at bbbfb91b517267bc3801a4ed2fb15d49e3140f27 had **one faulty casing assertion**. That assertion was corrected without changing the scene's continuity; one prose grammar error was also repaired before reader source-lock. Do not confuse an earlier passing local result with GitHub CI enrollment.
- The Python suite verifies all 21 reader components against source files and Git blob fingerprints, the first 20 manifest records unchanged, prior reader fingerprint, protected four 2026 hard-manuscript fingerprints and frozen 2016 archive fingerprint. The suite first passed **locally**; it was subsequently **enrolled** in branch Novel OS CI with an added source-exact 2016 causal chain step at commit 7bce6e822215704c39df70bd2b670a6bb25b4a72. GitHub CI completion must be checked at the eventual exact branch head; enrollment is not proof of a green run.
- Novel OS current source authority, execution-control and Bullpen command lifecycle were read. PR #188 is already merged, PR #243 is open/draft, PR #252 and #261 are open/draft with separate holds. No merge of any PR took place.

## Story-state delta, strictly NONCANON

After Mara's departure with Senn, someone exploits news that the shelter's keeper has gone. Black-circle claims are sold to strangers who believe the missing claimant's unissued entitlement may bring food, lodging or contents of a different woman's unretrieved chest. Esi investigates the circulation of the strips, declines Holl's conflation of separate claimants, and remains in sole practical custody of the working keys and surviving records.

During the diversion, **the brown incoming-supplies ledger with its pale repaired spine is stolen from the western room**. Len observes only a coat and a book's physical appearance; he does not identify a thief. The original claimant's private file and the 2016 historical archive remain separate and uncompromised; the sealed private message is not opened and the locked chest is not retrieved. Esi begins an actual surviving-document inventory and makes the loss public. Jake takes the first truthful notice to the market. Thief identity, organizer, motive, destination, Holl's involvement and the timing of any other deception remain unknown.

## Adversarial author-side objections / gates

1. **External intrigue over repetition:** Prior Chapters VI, IX and XII also featured misleading public notices or payments. The decisive new event is a stolen primary account book, not another mere correction. An independent editor should consider whether the first two movements linger too long on documents before the physical loss.
2. **Agency:** Esi makes independent managerial decisions, travels, handles surviving records, negotiates with Tern, and chooses disclosure. Jake stays inside a single permitted owner POV; Esi does not become a second interior narrator. Her competence must not be flattened into a lecturer's voice during revision.
3. **Mara's absence:** The attack closely follows her departure; this is a speculative coincidence or exploitation, not evidence of conspiracy by Senn, Mara or another established character. Her return is not promised and she is not restored midchapter.
4. **Claimant and locked chest:** Holl may be opportunistic, dishonest, misled or acting for a third person. No private mark has been authenticated to him, and the unretrieved chest belongs to a different woman. The private claimant file is NOT the stolen bound supplies ledger.
5. **Len's sight:** His injured eye is neither cured nor an absolute inability to observe; dialogue carefully separates seeing a brown spine from identifying a person. The carved bird is his independent project, not a magical clue.
6. **Material culture / geography:** Print technology, book binding, paper scraps, dye shed, market routes, wooden hinges, the public weigh-stones and Tern's binding offer are fictional proposals pending period material/Atlas review. An alleged public claim collector is not evidence of an approved Commonwealth tribunal, inheritance law or a new institution.
7. **Threat plausibility:** Theft occurs while the crowd is at the gate. It is feasible only if the western shelf can be reached from a kitchen door temporarily held off its latch. A physical-security and geography review must examine that path and the amount of traffic.
8. **Economic continuity:** One partial coin already posted remains a partial payment. Old supplier invoice, pledge remainder, unpaid refunds, damaged mill, unturned wheel and unsigned commission, bridge/cart, unknown courier and unaccepted upriver offer remain open.
9. **No invented ESPN truth:** The story contains no asserted real 2016 fantasy matchup, weekly result, final record, trade, opponent identification or real-person private motive. The G01_2016 source exists but is not proof historical scoring slot 1 belonged to human Jake.
10. **Promotion HOLD:** Tests and self-review are not an independent Authors Council/Umpire review. No human Founder approval, independent acceptance, 2026 manuscript changes, merge, publication or release has been performed.

## Next production gate

Request a genuine independent editorial/Character/Atlas/Umpire review of the expanded book, especially the repeated paper/claim mechanism and the causal link between Mara leaving and the theft. Continue NONCANON Chapter XXII only while review remains pending, developing a physical investigation that reveals consequential stakes without certifying a thief or contaminating historical ESPN fact. Consider enrolling the isolated historical reader test suite into a governed GitHub CI workflow in a separate explicitly tested change.
