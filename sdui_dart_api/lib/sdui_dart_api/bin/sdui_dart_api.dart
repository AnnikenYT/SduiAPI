import "package:http/http.dart";
import "package:shared_preferences/shared_preferences.dart";
import "dart:math";
import "dart:async";

unix2dt(final ts) {
  return DateTime.fromMillisecondsSinceEpoch(ts);
}

dt2unix(final dt) {
  return dt.millisecondsSinceEpoch;
}

check_data_age_sharedpref() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  int lastAge? = prefs.getInt("dataAge");

  if (lastAge == null) { 
    prefs.setInt("dataAge", dt2unix(DateTime.now())); 
    return True;
  }

  else {
    if (lastAge + (5 * 60 * 1000) < dt2unix(DateTime.now())) => return True;
    else => return False;
  }
}

check_data_age(final lastAge) {
  if (lastAge == null) { 
    prefs.setInt("dataAge", dt2unix(DateTime.now())); 
    return True;
  }

  else {
    if (lastAge + (5 * 60 * 1000) < dt2unix(DateTime.now())) => return True;
    else => return False;
  }
}

void main(List<String> arguments) {
  print(checkDataAge());
}
