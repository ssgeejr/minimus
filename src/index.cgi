#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;

my $q = CGI->new;
print $q->header('text/html');

# DB connection
my $dsn = "DBI:mysql:database=minimus;host=minimusdb";
my $db_user = "liono";
my $db_pass = "thundercats";  # Replace with your actual password
my $dbh = DBI->connect($dsn, $db_user, $db_pass, { RaiseError => 1, AutoCommit => 1 });

# Handle insert
if ($q->param('submit')) {
    my $name    = $q->param('name');
    my $email   = $q->param('email');
    my $phone   = $q->param('phone');
    my $company = $q->param('company');

    my $sth = $dbh->prepare("INSERT INTO userbase (real_name, email, phone_number, company_name) VALUES (?, ?, ?, ?)");
    $sth->execute($name, $email, $phone, $company);
}

# Fetch last 25 records
my $sth = $dbh->prepare("SELECT userid, real_name, email, phone_number, company_name, keyhash FROM userbase ORDER BY userid DESC LIMIT 25");
$sth->execute();

# Begin HTML output
print <<HTML;
<html>
<head>
    <title>Userbase Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        .form-section, .display-section {
            border: 1px solid red;
            padding: 20px;
            margin-bottom: 30px;
        }
        .form-section input[type="text"] {
            width: 300px;
            margin-bottom: 10px;
        }
        .form-section input[type="submit"] {
            padding: 5px 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background-color: #003366;
            color: white;
            text-align: left;
            padding: 8px;
        }
        td {
            padding: 8px;
            border: 1px solid red;
        }
    </style>
</head>
<body>

<div class="form-section">
    <h2>Enter New User</h2>
    <form method="post" action="index.cgi">
        <input type="text" name="name" placeholder="Full Name" required><br>
        <input type="text" name="email" placeholder="Email" required><br>
        <input type="text" name="phone" placeholder="Phone Number"><br>
        <input type="text" name="company" placeholder="Company Name"><br>
        <input type="submit" name="submit" value="Add User">
    </form>
</div>

<div class="display-section">
    <h2>Last 25 Users</h2>
    <table>
        <tr>
            <th>UserID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Company</th>
            <th>Hash</th>
        </tr>
HTML

my $row_count = 0;
while (my @row = $sth->fetchrow_array) {
    my $bgcolor = $row_count % 2 == 0 ? '#FFFFCC' : '#CCFFFF';
    print "<tr style=\"background-color: $bgcolor\">";
    for my $i (0..$#row) {
        my $style = $i == 0 ? 'style="font-weight: bold; color: #003366;"' : '';
        print "<td $style>$row[$i]</td>";
    }
    print "</tr>";
    $row_count++;
}

print <<HTML;
    </table>
</div>

</body>
</html>
HTML

$dbh->disconnect;
