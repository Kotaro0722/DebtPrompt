CREATE TABLE `debt`(
    `id` BIGINT PRIMARY KEY,
    `creditor` BIGINT,
    `debtor` BIGINT,
    `amount` INT,
    `ispay` BOOLEAN
)

CREATE  TABLE `total`(
    `id` BIGINT PRIMARY KEY,
    `message_id` BIGINT,
    `debt_id` BIGINT
)