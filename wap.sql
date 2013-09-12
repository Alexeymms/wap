-- wap: A minimalistic wireless billing system

-- Copyright(C) 2013 Global Reach Communications, Inc.
-- All Rights Reserved.

-- You have obtained a development version of this software in its source format.
-- You may not modify, redistribute or re-use this software under any circumstances,
-- including (but not limited to): selling, sublicensing, transferring owership,
-- creating derivative works, copying or reinstalling.  For more information, please
-- contact licensing@globalreachcomm.com

CREATE TABLE `cards` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `card` char(18) NOT NULL,
  `balance` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `i_product` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card` (`card`)
) ENGINE=InnoDB;

CREATE TABLE `ledger` (
  `i_user` bigint(20) unsigned NOT NULL DEFAULT '0',
  `i_card` bigint(20) unsigned NOT NULL DEFAULT '0',
  `type` enum('Credit','Debit','Activation') NOT NULL,
  `amount` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `reason` varchar(256) NOT NULL,
  `i_agent` bigint(20) unsigned NOT NULL DEFAULT '1',
  `session` varchar(64) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `session` (`session`)
) ENGINE=InnoDB;

CREATE TABLE `products` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `price` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `activation` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `fee` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `day` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `balance` decimal(10,6) NOT NULL DEFAULT '0.000000',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `email` (`email`)
) ENGINE=InnoDB;

CREATE TABLE `nas` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `identifier` char(30) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identifier` (`identifier`)
) ENGINE=InnoDB;

CREATE TABLE `nas_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;

CREATE TABLE `user_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;

CREATE TABLE `card_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;
