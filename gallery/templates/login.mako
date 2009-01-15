<form action='${h.url_for(controller="/login", action="submit")}' method="post" ENCTYPE="multipart/form-data">
	<table align=center>
		<tr>
			<td>user:</td>
			<td><input type=text name="username" maxlength=30 size=20 value="" ></td>
		</tr>
		<tr>
			<td>password:</td>
			<td><input type=password name="password" maxlength=30 size=20 value="" ></td>
		</tr>
        <tr>
            <td colspan=2><input name="enter" type="submit" value="Login"></td>
        </tr>

	</table>
</form>
