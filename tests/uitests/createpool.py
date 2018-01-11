from tests.uitests import utils as uiutils


class CreatePool(uiutils.UITestCase):
    """
    UI tests for the createpool wizard
    """

    ##############
    # Test cases #
    ##############

    def testCreatePool(self):
        # Open the createnet dialog
        hostwin = self._open_host_window("Storage")
        hostwin.find_pattern("pool-add", "push button").click()
        win = self.app.root.find_pattern(
                "Add a New Storage Pool", "frame")

        # Create a simple default dir pool
        newname = "a-test-new-pool"
        forward = win.find_pattern("Forward", "push button")
        finish = win.find_pattern("Finish", "push button")
        name = win.find_pattern(None, "text", "Name:")
        name.text = newname
        forward.click()
        finish.click()

        # Select the new object in the host window, then do
        # stop->start->stop->delete, for lifecycle testing
        uiutils.check_in_loop(lambda: hostwin.active)
        cell = hostwin.find_pattern(newname, "table cell")
        delete = hostwin.find_pattern("pool-delete", "push button")
        start = hostwin.find_pattern("pool-start", "push button")
        stop = hostwin.find_pattern("pool-stop", "push button")

        cell.click()
        stop.click()
        uiutils.check_in_loop(lambda: start.sensitive)
        start.click()
        uiutils.check_in_loop(lambda: stop.sensitive)
        stop.click()
        uiutils.check_in_loop(lambda: delete.sensitive)

        # Delete it
        delete.click()
        alert = self.app.root.find_pattern("vmm dialog", "alert")
        alert.find_fuzzy("permanently delete the pool", "label")
        alert.find_pattern("Yes", "push button").click()

        # Ensure it's gone
        uiutils.check_in_loop(lambda: cell.dead)


        # Test a scsi pool
        hostwin.find_pattern("pool-add", "push button").click()
        uiutils.check_in_loop(lambda: win.active)
        typ = win.find_pattern(None, "combo box", "Type:")
        newname = "a-scsi-pool"
        name.text = "a-scsi-pool"
        typ.click()
        win.find_fuzzy("SCSI Host Adapter", "menu item").click()
        forward.click()
        finish.click()
        hostwin.find_pattern(newname, "table cell")

        # Test a ceph pool
        hostwin.find_pattern("pool-add", "push button").click()
        uiutils.check_in_loop(lambda: win.active)
        newname = "a-ceph-pool"
        name.text = "a-ceph-pool"
        typ.click()
        win.find_fuzzy("RADOS Block", "menu item").click()
        forward.click()
        win.find_fuzzy(None, "text", "Host Name:").text = "example.com:1234"
        win.find_fuzzy(None, "text", "Source Name:").typeText("frob")
        finish.click()
        hostwin.find_pattern(newname, "table cell")

        # Ensure host window closes fine
        hostwin.click()
        hostwin.keyCombo("<ctrl>w")
        uiutils.check_in_loop(lambda: not hostwin.showing and
                not hostwin.active)