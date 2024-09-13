CREATE TABLE `debt`(
    `id` BIGINT PRIMARY KEY,
    `creditor` BIGINT,
    `debtor` BIGINT,
    `amount` INT,
    `ispay` BOOLEAN
)