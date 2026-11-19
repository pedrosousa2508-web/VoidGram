/*
 * VoidGram — cliente Android não oficial do Telegram.
 * Distribuído sob a GNU GPL versão 2 ou posterior, como a base Telegram.
 */
package org.telegram.ui;

import android.content.Context;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;

import org.telegram.messenger.BuildVars;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.messenger.browser.Browser;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.Cells.HeaderCell;
import org.telegram.ui.Cells.ShadowSectionCell;
import org.telegram.ui.Cells.TextCell;
import org.telegram.ui.Cells.TextInfoPrivacyCell;

/** Tela "VoidGram" nas Configurações: versão, origem do código e licença. */
public class VoidGramSettingsActivity extends BaseFragment {

    private static final String SOURCE_URL = "https://github.com/pedrosousa2508-web/VoidGram";
    private static final String LICENSE_URL = SOURCE_URL + "/blob/main/LICENSE";

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(LocaleController.getString(R.string.VoidGramSettings));
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        ScrollView scrollView = new ScrollView(context);
        scrollView.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundGray));
        LinearLayout list = new LinearLayout(context);
        list.setOrientation(LinearLayout.VERTICAL);
        scrollView.addView(list, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.WRAP_CONTENT));

        addHeader(context, list, LocaleController.getString(R.string.VoidGramInfoHeader));
        addValue(context, list, LocaleController.getString(R.string.VoidGramVersionTitle),
                context.getString(R.string.VoidGramVersion), true);
        addValue(context, list, LocaleController.getString(R.string.VoidGramBaseTitle),
                BuildVars.BUILD_VERSION_STRING, true);
        addValue(context, list, LocaleController.getString(R.string.VoidGramUpstreamTitle),
                context.getString(R.string.VoidGramUpstreamCommit), false);
        addView(list, new ShadowSectionCell(context));

        addHeader(context, list, LocaleController.getString(R.string.VoidGramLinksHeader));
        addLink(context, list, LocaleController.getString(R.string.VoidGramSourceCode), SOURCE_URL, true);
        addLink(context, list, LocaleController.getString(R.string.VoidGramLicense), LICENSE_URL, false);

        TextInfoPrivacyCell notice = new TextInfoPrivacyCell(context);
        notice.setText(LocaleController.getString(R.string.VoidGramNotice));
        addView(list, notice);

        fragmentView = scrollView;
        return fragmentView;
    }

    private static void addView(LinearLayout list, View view) {
        list.addView(view, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
    }

    private static void addHeader(Context context, LinearLayout list, String text) {
        HeaderCell cell = new HeaderCell(context);
        cell.setText(text);
        cell.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));
        addView(list, cell);
    }

    private static void addValue(Context context, LinearLayout list, String title, String value, boolean divider) {
        TextCell cell = new TextCell(context);
        cell.setTextAndValue(title, value, divider);
        cell.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));
        addView(list, cell);
    }

    private void addLink(Context context, LinearLayout list, String title, String url, boolean divider) {
        TextCell cell = new TextCell(context);
        cell.setText(title, divider);
        cell.setBackground(Theme.getSelectorDrawable(true));
        cell.setOnClickListener(v -> Browser.openUrl(getParentActivity(), url));
        addView(list, cell);
    }
}
