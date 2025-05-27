<?php

namespace App\Notifications;

use App\Models\Setting;
use Illuminate\Bus\Queueable;
use Illuminate\Notifications\Channels\SlackWebhookChannel;
use Illuminate\Notifications\Messages\SlackMessage;
use Illuminate\Notifications\Notification;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use NotificationChannels\MicrosoftTeams\MicrosoftTeamsChannel;
use NotificationChannels\MicrosoftTeams\MicrosoftTeamsMessage;

class AuditNotification extends Notification
{
    use Queueable;

    private $params;
    protected $settings;

    public function __construct($params)
    {
        $this->settings = Setting::getSettings();
        $this->params = $params;
    }

    public function via()
    {
        $notifyBy = [];
        if ($this->settings->webhook_selected == 'slack' || $this->settings->webhook_selected == 'general') {
            Log::debug('use webhook');
            $notifyBy[] = SlackWebhookChannel::class;
        }
        if ($this->settings->webhook_selected == 'microsoft' && $this->settings->webhook_endpoint) {
            $notifyBy[] = MicrosoftTeamsChannel::class;
        }
        return $notifyBy;
    }

    public function toSlack()
    {
        $channel = $this->settings->webhook_channel ?: '';
        $item = $this->params['item'];
        $admin_user = $this->params['admin'];

        // Ambil data user terakhir yang checkout
        $assignedUser = optional($item->assignedTo);
        $lastUserName = $assignedUser->present()->fullName() ?? 'Belum ada';
        $lastUserUrl = $assignedUser->present()->viewUrl() ?? '#';

        $fields = [
            '🛠️ By' => '<' . $admin_user->present()->viewUrl() . '|' . $admin_user->present()->fullName() . '>',
            '👤 User' => '<' . $lastUserUrl . '|' . $lastUserName . '>',
        ];

        if (array_key_exists('note', $this->params)) {
            $fields['📝 Note'] = $this->params['note'];
        }

        if (array_key_exists('location', $this->params)) {
            $fields['📍 Location'] = $this->params['location'];
        }

        return (new SlackMessage)
            ->success()
            ->content(class_basename(get_class($item)) . ' Audited')
            ->from($this->settings->webhook_botname ?: 'Snipe-Bot')
            ->to($channel)
            ->attachment(function ($attachment) use ($item, $fields) {
                $attachment->title($item->present()->name, $item->present()->viewUrl())
                           ->fields($fields);
            });
    }

    public static function toMicrosoftTeams($params)
    {
        $item = $params['item'];
        $admin_user = $params['admin'];
        $note = $params['note'] ?? '';
        $location = $params['location'] ?? '';
        $setting = Setting::getSettings();

        // Last checkout untuk Teams
        $lastUser = optional($item->assignedTo);

        $lastUserName = $lastUser->present()->fullName() ?? 'Belum ada';

        if (!Str::contains($setting->webhook_endpoint, 'workflows')) {
            return MicrosoftTeamsMessage::create()
                ->to($setting->webhook_endpoint)
                ->type('success')
                ->title(class_basename(get_class($item)) . ' Audited')
                ->addStartGroupToSection('activityText')
                ->fact(trans('mail.asset'), $item->present()->name)
                ->fact(trans('general.administrator'), $admin_user->present()->viewUrl() . '|' . $admin_user->present()->fullName())
                ->fact('User', $lastUserName);
        }

        $message = class_basename(get_class($item)) . ' Audited By ' . $admin_user->present()->fullName();
        $details = [
            trans('mail.asset') => htmlspecialchars_decode($item->present()->name),
            trans('mail.notes') => $note,
            trans('general.location') => $location,
            'User' => $lastUserName,
        ];

        return [$message, $details];
    }
}