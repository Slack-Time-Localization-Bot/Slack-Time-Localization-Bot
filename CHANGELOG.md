# Changelog

## [v0.1.10](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.10) (2024-03-02)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.9...v0.1.10)

**Merged pull requests:**

- Move tests to own directory to prevent distortion of coverage percentage [\#25](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/25) ([phihos](https://github.com/phihos))
- Do not show timezone localization if timezones have the same UTC offset \(like Europe/Amsterdam and CE\(S\)T\) [\#24](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/24) ([phihos](https://github.com/phihos))
- Better formatting for time intervals like "starting between at 5:00 and 7:00" [\#23](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/23) ([phihos](https://github.com/phihos))
- Support message edits by posting a new ephemeral message upon edit [\#22](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/22) ([phihos](https://github.com/phihos))
- Minor improvement in message handling testing [\#21](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/21) ([phihos](https://github.com/phihos))

## [v0.1.9](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.9) (2024-03-01)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.8...v0.1.9)

**Merged pull requests:**

- Omit UTC time from message if original temporal expression already was in UTC [\#20](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/20) ([phihos](https://github.com/phihos))
- Split fake intervals like "15:00 \(UTC\) / 16:00 \(CET\)" into separate expressions [\#19](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/19) ([phihos](https://github.com/phihos))
- Support timezones in round braces like \("15:00 \(UTC\)"\) [\#18](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/18) ([phihos](https://github.com/phihos))

## [v0.1.8](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.8) (2024-02-29)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.7...v0.1.8)

**Merged pull requests:**

- Support half-intervals \("since 9:00", "until 9:00"\) [\#17](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/17) ([phihos](https://github.com/phihos))

## [v0.1.7](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.7) (2024-02-29)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.6...v0.1.7)

**Merged pull requests:**

- Improve language detection for short texts and fall back to English if uncertain [\#16](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/16) ([phihos](https://github.com/phihos))

## [v0.1.6](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.6) (2024-02-28)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.5...v0.1.6)

**Merged pull requests:**

- Interpret time expressions in 24-hour format by default [\#15](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/15) ([phihos](https://github.com/phihos))

## [v0.1.5](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.5) (2024-02-28)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.4...v0.1.5)

**Merged pull requests:**

- Evaluate time intervals with beginning and end [\#14](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/14) ([phihos](https://github.com/phihos))
- Bump cachetools from 5.3.2 to 5.3.3 [\#13](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/13) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump black from 23.12.1 to 24.2.0 [\#12](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/12) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 8.0.1 to 8.0.2 [\#11](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/11) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v0.1.4](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.4) (2024-02-25)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.3...v0.1.4)

**Merged pull requests:**

- Fix --debug flag not working introduced by previous PR [\#10](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/10) ([phihos](https://github.com/phihos))
- Add tests for message handling [\#9](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/9) ([phihos](https://github.com/phihos))
- Add test coverage to CI [\#8](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/8) ([phihos](https://github.com/phihos))
- Send ephemeral message response into thread if message came from thread [\#7](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/7) ([phihos](https://github.com/phihos))
- Add new env var parameters USER\_CACHE\_SIZE and USER\_CACHE\_TTL [\#6](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/6) ([phihos](https://github.com/phihos))

## [v0.1.3](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.3) (2024-02-22)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.2...v0.1.3)

**Merged pull requests:**

- Only accept duckling responses of type "value" [\#5](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/5) ([phihos](https://github.com/phihos))

## [v0.1.2](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.2) (2024-02-22)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.1...v0.1.2)

**Merged pull requests:**

- Fetch users on-demand and not all users on first message [\#4](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/4) ([phihos](https://github.com/phihos))

## [v0.1.1](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.1) (2024-02-22)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.0...v0.1.1)

**Merged pull requests:**

- Add debug flag [\#3](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/3) ([phihos](https://github.com/phihos))
- Provide CLI entrypoint [\#2](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/2) ([phihos](https://github.com/phihos))

## [v0.1.0](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.0) (2024-02-22)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/v0.1.0-dev1...v0.1.0)

## [v0.1.0-dev1](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/tree/v0.1.0-dev1) (2024-02-22)

[Full Changelog](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/compare/5121b09df4bdb4d61de7d7309b24a307dda99e7f...v0.1.0-dev1)

**Merged pull requests:**

- Make CI pipeline work [\#1](https://github.com/Slack-Time-Localization-Bot/Slack-Time-Localization-Bot/pull/1) ([phihos](https://github.com/phihos))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
