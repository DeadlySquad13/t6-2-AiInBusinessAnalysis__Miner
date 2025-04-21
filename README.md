<!-- toc -->

# AI in Business Analysis. Miner
Mining conferences data for educational purposes.

Uses self-made caching for fetching data (in [data/raw](./data/raw)). Delete folder if you
want to refetch new data.

All processed data is in [processed folder](./data/processed).

## [Methodology chosen][2]
[Data Science Lifecycle Process][1].
See [Branch Types][3] for branching naming model.

If working in data science workflow, a jira ticket can be used instead of issue number when creating Data Science Lifecycle Process branches
(`<ProjectAbbreviation>-#`). Also a `_` is used as delimiter between
branch type + number and description of the branch. For example,
experiment and model branches made while working on RAN-73 will be:
`experiment/RAN-73_classification-EBM`
`model/RAN-73_custom-churn-classification`

## Contributing
See guidelines in [Contributing](./CONTRIBUTING.md). This projects also
has Docker support, see ["Running in Docker"
section in Contributing](./CONTRIBUTING.md#running-in-docker).

## References
[1]: <https://github.com/dslp/dslp> 'Data Science Lifecycle Process'
[2]: <https://youtu.be/nx1VQrGfU8A?t=556> 'Data Science Lifecycle Process
Lecture'
[3]: <https://github.com/dslp/dslp/blob/main/branching/branch-types.md> 'Data
Science Lifecycle Branch Types'
