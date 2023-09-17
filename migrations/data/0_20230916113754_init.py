from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `access_token` (
    `access_token` CHAR(36) NOT NULL  PRIMARY KEY,
    `waktu_basi` DATETIME(6) NOT NULL,
    `user_id` VARCHAR(225) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `logaudio` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `audio_id` INT NOT NULL,
    `user_id` VARCHAR(225) NOT NULL,
    `transcript` VARCHAR(225) NOT NULL,
    `translate` VARCHAR(225) NOT NULL,
    `audio_streming` VARCHAR(225) NOT NULL,
    `audio_download` VARCHAR(225) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `logpercakapan` (
    `id_percakapan` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` VARCHAR(225) NOT NULL,
    `input` VARCHAR(225) NOT NULL,
    `output` VARCHAR(225) NOT NULL,
    `translate` VARCHAR(225) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userdata` (
    `user_id` CHAR(36) NOT NULL  PRIMARY KEY,
    `nama` VARCHAR(225),
    `email` VARCHAR(225) NOT NULL,
    `password` LONGBLOB,
    `akunwso` BOOL NOT NULL  DEFAULT 0,
    `premium` BOOL NOT NULL  DEFAULT 0,
    `waktu_basi_premium` DATETIME(6),
    `token_konfirmasi` VARCHAR(225),
    `status` BOOL NOT NULL  DEFAULT 0,
    `ban` BOOL NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
