-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 14, 2026 at 01:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `keuangan`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('income','expense') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `type`, `created_at`) VALUES
(7, 'Gaji', 'income', '2026-04-16 11:48:42'),
(8, 'Bonus', 'income', '2026-04-16 11:48:42'),
(9, 'Investasi', 'income', '2026-04-16 11:48:42'),
(10, 'Makanan', 'expense', '2026-04-16 11:48:42'),
(11, 'Transportasi', 'expense', '2026-04-16 11:48:42'),
(12, 'Belanja', 'expense', '2026-04-16 11:48:42'),
(13, 'Tagihan Listrik', 'expense', '2026-04-16 11:48:42'),
(14, 'Internet', 'expense', '2026-04-16 11:48:42'),
(15, 'Bonus tahunan', 'income', '2026-04-23 13:10:28');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `total_income` decimal(15,2) DEFAULT 0.00,
  `total_expense` decimal(15,2) DEFAULT 0.00,
  `balance` decimal(15,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`id`, `user_id`, `month`, `year`, `total_income`, `total_expense`, `balance`, `created_at`) VALUES
(1, 2, 4, 2026, 6000000.00, 825000.00, 5175000.00, '2026-04-16 11:49:53');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `type` enum('income','expense') NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `description` text DEFAULT NULL,
  `transaction_date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `user_id`, `category_id`, `type`, `amount`, `description`, `transaction_date`, `created_at`) VALUES
(22, 2, 7, 'income', 5000000.00, 'Gaji Bulanan', '2026-04-01', '2026-04-16 11:54:41'),
(23, 2, 8, 'income', 1000000.00, 'Bonus Proyek', '2026-04-05', '2026-04-16 11:54:41'),
(24, 2, 10, 'expense', 75000.00, 'Makan Siang', '2026-04-06', '2026-04-16 11:54:41'),
(25, 2, 11, 'expense', 50000.00, 'Transportasi Online', '2026-04-07', '2026-04-16 11:54:41'),
(26, 2, 12, 'expense', 250000.00, 'Belanja Bulanan', '2026-04-08', '2026-04-16 11:54:41'),
(27, 2, 13, 'expense', 150000.00, 'Pembayaran Listrik', '2026-04-10', '2026-04-16 11:54:41'),
(28, 2, 14, 'expense', 300000.00, 'Tagihan Internet', '2026-04-12', '2026-04-16 11:54:41'),
(29, 2, 7, 'income', 6700001.00, '', '2026-04-18', '2026-04-18 12:13:14'),
(30, 3, 7, 'income', 6000000.00, 'Gaji bulan april 2026', '2026-04-30', '2026-05-14 11:27:40'),
(31, 3, 8, 'income', 2000000.00, 'Bonus bulan april', '2026-04-30', '2026-05-14 11:28:33'),
(32, 3, 9, 'income', 1400000.00, 'Profit saham bulan apri', '2026-04-30', '2026-05-14 11:29:33');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'admin@gmail.com', 'admin', 'admin', '2026-04-16 11:48:13', '2026-04-16 11:48:13'),
(2, 'Rangga Ivan', 'rangga@gmail.com', '12345', 'user', '2026-04-16 11:48:13', '2026-04-16 11:48:13'),
(3, 'Rangga', 'rngga27@gmail.com', '6f36970c36998c6dd5a67e5020971fdd651d8a5c7c207e22edfec91d77b84cfa', 'user', '2026-05-14 11:06:49', '2026-05-14 11:06:49');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
