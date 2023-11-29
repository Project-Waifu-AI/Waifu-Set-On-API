from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `karakter` (
    `nama` VARCHAR(225) NOT NULL  PRIMARY KEY,
    `bahasaYangDigunakan` VARCHAR(225) NOT NULL,
    `informasi_tambahan` JSON,
    `speakerID` JSON
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `logaudio` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `audio_id` INT NOT NULL,
    `email` VARCHAR(320) NOT NULL,
    `transcript` VARCHAR(225) NOT NULL,
    `translate` VARCHAR(225) NOT NULL,
    `audio_streming` VARCHAR(225) NOT NULL,
    `audio_download` VARCHAR(225) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `logpercakapan` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `id_percakapan` INT NOT NULL,
    `email` VARCHAR(320) NOT NULL,
    `input` VARCHAR(225) NOT NULL,
    `output` LONGTEXT NOT NULL,
    `translate` VARCHAR(225) NOT NULL,
    `audio_streming` VARCHAR(225) NOT NULL,
    `audio_download` VARCHAR(225) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `token_google` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(320) NOT NULL,
    `access_token` VARCHAR(255) NOT NULL,
    `token_exp` DATETIME(6) NOT NULL,
    `refersh_token` VARCHAR(255)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userdata` (
    `email` VARCHAR(320) NOT NULL  PRIMARY KEY,
    `nama` VARCHAR(225),
    `admin` BOOL NOT NULL  DEFAULT 0,
    `ulang_tahun` DATE,
    `gender` VARCHAR(10),
    `password` LONGBLOB,
    `AtsumaruKanjo` INT NOT NULL  DEFAULT 0,
    `NegaiGoto` INT NOT NULL  DEFAULT 0,
    `karakterYangDimiliki` JSON,
    `akunwso` BOOL NOT NULL  DEFAULT 0,
    `googleAuth` BOOL NOT NULL  DEFAULT 0,
    `driveID` VARCHAR(320),
    `token_konfirmasi` VARCHAR(225),
    `premium_token` VARCHAR(225),
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
