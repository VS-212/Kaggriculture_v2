# Official Kaggriculture rules — source extract

Snapshot checked **2026-08-17 UTC** from:
<https://www.kaggle.com/competitions/kaggriculture/rules>.

This file preserves the operative English wording used by the audit. It is not a
substitute for the complete live legal text: eligibility, privacy, tax,
indemnity and other boilerplate remain binding even where not reproduced here.
Section labels follow the page; Kaggle's page contains both Foundational and
General Competition Rules and has some repeated numbering.

## Binding agreement and precedence

> ENTRY IN THIS COMPETITION CONSTITUTES YOUR ACCEPTANCE OF THESE OFFICIAL
> COMPETITION RULES.

> You cannot sign up to Kaggle from multiple accounts and therefore you cannot
> enter or submit from multiple accounts.

Under **Kaggle Competition Foundational Rules (Non-editable)**:

> Competition participants must also agree to Kaggle's Foundational Competition
> Rules. These rules will supersede the competition-specific rules in the event
> of any conflict.

## 1. Competition-Specific Terms

- **Competition title:** Kaggriculture
- **Sponsor:** Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043
- **Total prizes:** $50,000; First through Tenth Prize are $5,000 each
- **Winner license type:** CC-BY 4.0
- **Data access and use:** Apache 2.0

## 2.1 Team Limits

> a. The maximum Team size is five (5).
>
> b. Team mergers are allowed and can be performed by the Team leader. In order
> to merge, the combined Team must have a total Submission count less than or
> equal to the maximum allowed as of the Team Merger Deadline. The maximum
> allowed is the number of Submissions per day multiplied by the number of days
> the competition has been running.

## 2.2 Submission Limits

> a. You may submit a maximum of five (5) Submissions per day.
>
> b. You may select up to two (2) Final Submissions for judging.

The live Overview adds an operational statement not present in this clause:

> To reduce the number of bots playing and ensure high-quality matching, only
> the latest 2 submissions are tracked. The latest 2 submissions are also used
> for final leaderboard evaluation.

Because those statements are not worded identically, keep the desired finals as
the newest two and verify the competition UI before the deadline.

## 2.4 Competition Data

> You may access and use the Competition Data for any purpose, whether
> commercial or non-commercial, including for participating in the Competition
> and on Kaggle.com forums, and for academic research and education.

The next security clause is narrower and easy to miss:

> You agree to use reasonable and suitable measures to prevent persons who have
> not formally agreed to these Rules from gaining access to the Competition
> Data. You agree not to transmit, duplicate, publish, redistribute or otherwise
> provide or make available the Competition Data to any party not participating
> in the Competition. You agree to notify Kaggle immediately upon learning of
> any possible unauthorized transmission of or unauthorized access to the
> Competition Data and agree to work with Kaggle to rectify any unauthorized
> transmission or access.

## 2.5 Winner License

> Open Source: You hereby license and will license your winning Submission and
> the source code used to generate the Submission under CC-BY 4.0 an Open Source
> Initiative-approved license [...] that in no event limits commercial use of
> such code or model containing or depending on such code.

The rule exempts generally available third-party commercial software from being
relicensed and says input data or pretrained models with an incompatible license
do not themselves need the preceding open-source grant. It also states:

> You may be required by the Sponsor to provide a detailed description of how
> the winning Submission was generated [...] where one must be able to reproduce
> the approach by reading the description [...] The description should also
> include a link to a code repository with complete and detailed instructions so
> that the results obtained can be reproduced. After your solution has been
> validated, you may be asked to discuss your results via a recorded call or
> panel call with the competition sponsors.

## 2.6 External Data and Tools

> You may use data other than the Competition Data (“External Data”) to develop
> and test your Submissions. However, you will ensure the External Data is either
> publicly available and equally accessible to use by all Participants of the
> Competition for purposes of the competition at no cost to the other
> Participants, or satisfies the Reasonableness criteria [...].

> The use of external data and models is acceptable unless specifically
> prohibited by the Host. [...] their use must be “reasonably accessible to all”
> and of “minimal cost”.

The page explicitly includes LLMs in its reasonableness test:

> Are Participants being excluded from a competition because of the “excessive”
> costs for access to certain LLMs, external data, or tools that might be used by
> other Participants.

It gives a small subscription such as Gemini Advanced as a potentially
reasonable example and a proprietary dataset costing more than a prize as an
unreasonable example. It separately permits AutoML tools where the participant
has a license compatible with all Competition Rules.

## 2.10 Scoring and Leaderboard

> Your Submissions will be scored based on their performance in an episode, and
> your performances in episodes will be aggregated to determine your position on
> the Leaderboard, in each case as described in the evaluation documentation on
> the Competition Website. There is no Private Leaderboard in Simulation
> competitions.

## 2.11 Environments & Public Availability

> This Competition makes use of Kaggle Environments. Additional rules related to
> the Environment(s) used in this Competition are available on the Competition
> Website. A replay of each episode of the competition, which includes the
> actions taken by your Submission in the episode, may be publicly available and
> downloadable.

## 2.12 No Ingress or Egress

> During the evaluation of an episode your Submission may not pull in or use any
> information external to the Submission and Environment and may not send any
> information out.

This is the direct rule prohibiting external inference APIs, runtime downloads
and telemetry during a game.

## General Rules 3.5 — Individuals and Teams

> Individual Account. You may make Submissions only under one, unique Kaggle.com
> account. You will be disqualified if you make Submissions through more than
> one Kaggle account, or attempt to falsify an account to act as your proxy.

> Teams. [...] you may join or form only one Team. Each Team member must be a
> single individual with a separate Kaggle account. You must register
> individually for the Competition before joining a Team.

> Private Sharing. No private sharing outside of Teams. Privately sharing code
> or data outside of Teams is not permitted. It's okay to share code if made
> available to all Participants on the forums.

## General Rules 3.6 — Submission Code Requirements

> Private Code Sharing. [...] during the Competition Period, you are not allowed
> to privately share source or executable code developed in connection with or
> based upon the Competition Data or other source or executable code relevant to
> the Competition (“Competition Code”). This prohibition includes sharing
> Competition Code between separate Teams, unless a Team merger occurs.

> Public Code Sharing. [...] If you do choose to share Competition Code or other
> such code, you are required to share it on Kaggle.com on the discussion forum
> or notebooks associated specifically with the Competition for the benefit of
> all competitors. By so sharing, you are deemed to have licensed the shared
> code under an Open Source Initiative-approved license [...] that in no event
> limits commercial use [...].

> Use of Open Source. [...] you must only use open source code licensed under an
> Open Source Initiative-approved license [...] that in no event limits
> commercial use of such code or model containing or depending on such code.

## General Rules 3.8–3.10 — Winner response, remediation and tax

- A potential winner must respond to notification within one week.
- Requested prize-acceptance documents must be returned within two weeks.
- On non-compliance the Sponsor may disqualify the submission or require
  remediation within one week, including resolving license conflicts.
- Team prize money is split evenly unless all members unanimously notify Kaggle
  of another split before payment.
- Taxes on prizes are the winners' responsibility.

## Eligibility extract

The live rules require a registered Kaggle account; the older of age 18 or the
age of majority unless the Sponsor has agreed otherwise; and compliance with
U.S. export controls and sanctions. They exclude residents of Crimea, so-called
DNR or LNR, Cuba, Iran and North Korea and persons/entities under applicable U.S.
sanctions. Local law and employer/entity policies may add restrictions.
Competition Entity employees and contractors may participate subject to policy
but are not prize-eligible unless stated otherwise.

Read the complete current eligibility and legal clauses before accepting:
<https://www.kaggle.com/competitions/kaggriculture/rules>.
