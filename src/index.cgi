#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;

my $q = CGI->new;
print $q->header('text/html');

# Database config
my $dsn = "DBI:mysql:database=minimus;host=minimusdb";
my $db_user = "liono";
my $db_pass = "thundercats";

my $dbh = DBI->connect($dsn, $db_user, $db_pass, { RaiseError => 1, AutoCommit => 1 });

# Handle delete
if ($q->param('delete_id')) {
    my $sth = $dbh->prepare("DELETE FROM userbase WHERE userid = ?");
    $sth->execute($q->param('delete_id'));
}

# Handle edit
my ($edit_id, $edit_user);
if ($q->param('edit_id')) {
    $edit_id = $q->param('edit_id');
    my $sth = $dbh->prepare("SELECT real_name, email, phone_number, company_name FROM userbase WHERE userid = ?");
    $sth->execute($edit_id);
    $edit_user = $sth->fetchrow_hashref;
}

# Handle insert/update
if ($q->param('submit')) {
    my ($name, $email, $phone, $company, $userid) = map { $q->param($_) } qw(name email phone company userid);
    if ($userid) {
        my $sth = $dbh->prepare("UPDATE userbase SET real_name = ?, email = ?, phone_number = ?, company_name = ? WHERE userid = ?");
        $sth->execute($name, $email, $phone, $company, $userid);
    } else {
        my $sth = $dbh->prepare("INSERT INTO userbase (real_name, email, phone_number, company_name) VALUES (?, ?, ?, ?)");
        $sth->execute($name, $email, $phone, $company);
    }
}

# Fetch the last 25 users
my $sth = $dbh->prepare("SELECT userid, real_name, email, phone_number, company_name, keyhash FROM userbase ORDER BY userid DESC LIMIT 25");
$sth->execute();

# Output HTML
print <<HTML;
<html>
<head>
    <title>Userbase Viewer</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<div class="form-section">
    <h2>@{[$edit_user ? "Edit User" : "Enter New User"]}</h2>
    <form method="post" action="index.cgi">
        <input type="hidden" name="userid" value="@{[$edit_id // '']}">
        <input type="text" name="name" placeholder="Full Name" value="@{[$edit_user->{real_name} // '']}" required><br>
        <input type="text" name="email" placeholder="Email" value="@{[$edit_user->{email} // '']}" required><br>
        <input type="text" name="phone" placeholder="Phone Number" value="@{[$edit_user->{phone_number} // '']}"><br>
        <input type="text" name="company" placeholder="Company Name" value="@{[$edit_user->{company_name} // '']}"><br>
        <input type="submit" name="submit" value="@{[$edit_id ? 'Update User' : 'Add User']}">
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
            <th>Actions</th>
        </tr>
HTML

my $row_count = 0;
while (my @row = $sth->fetchrow_array) {
    my $bgcolor = $row_count++ % 2 == 0 ? '#FFFFCC' : '#CCFFFF';
    print qq{<tr style="background-color: $bgcolor">};
    for my $i (0..$#row) {
        my $style = $i == 0 ? 'style="font-weight: bold; color: #003366;"' : '';
        print "<td $style>$row[$i]</td>";
    }

    # Action buttons
    print qq{
        <td>
            <form method="post" action="index.cgi" style="display:inline;">
                <input type="hidden" name="edit_id" value="$row[0]">
                <input type="submit" value="Edit">
            </form>
            <form method="post" action="index.cgi" style="display:inline;" onsubmit="return confirm('Delete this user?');">
                <input type="hidden" name="delete_id" value="$row[0]">
                <input type="submit" value="Delete">
            </form>
        </td>
    };
    print "</tr>";
}

print <<HTML;
    </table>
</div>

</body>
</html>
HTML

$dbh->disconnect;
