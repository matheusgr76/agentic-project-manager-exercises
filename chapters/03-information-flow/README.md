# Chapter 3 — map the information flow

**Compare your work:** Use [Records 1–6 in CSV](source-records.csv), then compare your source map and two reports with the [worked example](example-output.md).

**Tools:** a spreadsheet or text document and a chatbot. No integration or programming is needed.

## Exercise

1. Use [Records 1–6](../../acme-practice-packet/records-chapters-1-3.md#chapter-3--information-flow-map). Map five information needs: progress, product decisions, dependencies, capacity, and customer commitments. For each, record source and day, apparent owner, freshness requirement, and response to missing information.
2. Before using AI, decide what you would report about Bravo's estimate, the data decision, and capacity. Identify who you would contact before declaring the dependency resolved.
3. Ask the assistant for a source-cited information-flow table and a fact sheet of at most 180 words. Tell it that informal agreement is not approval and provisional capacity is not confirmed availability.
4. Review the fact sheet. Use only the verified version to draft a management update and an engineering update, each at most 130 words. Compare every factual claim across the two versions.
5. Choose one change to test next week. Classify the work as retain, simplify, assist, or automate. Measure full preparation and checking time before claiming a saving.

## Check the result

Both reports may emphasize different decisions, but neither may turn Record 3 into approval, Record 4 into confirmed availability, or the 25% target into a release commitment. The result should include an information-flow map, fact sheet, two draft reports, and unresolved questions.

The [reporting samples](../../acme-practice-packet/reporting-samples.md) show a similar pattern using the **different Chapter 4 snapshot**. Do not merge their dates or issue states into this chapter's records.

## Copyable starter prompts

~~~text
Using only Acme Records 1–6 below, make an information-flow table with: information needed, source and date, apparent owner, confirmed statement, missing information or conflict, verification question, and reporting consequence. Then draft a fact sheet of at most 180 words. Cite record numbers. Do not infer formal approval from the Teams discussion or confirmed availability from provisional capacity. Show conflicts rather than selecting a convenient version.

Records 1–6:
[Paste records.]
~~~

After you verify the fact sheet:

~~~text
Using only this verified fact sheet, draft a management update and an engineering coordination update, each at most 130 words. Change emphasis to fit the audience, but add no new facts, owners, dates, or commitments. List any factual claims appearing in only one version.

Verified fact sheet:
[Paste your reviewed text.]
~~~
